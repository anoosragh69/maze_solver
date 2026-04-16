from pyamaze import maze, agent
from utils import to_path, generate_penalty_zones, evaluate_path
from ga import run_ga
import matplotlib.pyplot as plt
import multiprocessing as mp
import sys

def plot_path_comparison(fastest, cheapest, balanced, output_file='path_comparison.png'):
    labels = ['Fastest', 'Cheapest', 'Balanced']
    times = [fastest['time'], cheapest['time'], balanced['time']]
    costs = [fastest['cost'], cheapest['cost'], balanced['cost']]

    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar([i - width/2 for i in x], times, width, label='Time', color='skyblue')
    rects2 = ax.bar([i + width/2 for i in x], costs, width, label='Cost', color='salmon')

    ax.set_ylabel('Score')
    ax.set_title('Path Comparison: Time vs Cost')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    if hasattr(ax, 'bar_label'):
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    # Always write the chart so results are available even on headless/flaky GUI setups.
    fig.savefig(output_file, dpi=150)
    print(f"Saved comparison chart to: {output_file}")

    try:
        plt.show()
    except Exception as e:
        print(f"Could not open plot window ({e}). Check the saved chart file instead.")

def main():
    rows, cols = 10, 10
    print(f"Creating a {rows}x{cols} maze...")
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=100)

    time_zones, cost_zones = generate_penalty_zones(rows, cols, time_prob=0.3, cost_prob=0.3)

    print("Running GA to learn valid path population...")
    population = run_ga(m, generations=150, population_size=400)

    valid_paths = []
    for chrom in population:
        p_dict, p_list = to_path(chrom, m)
        if p_list[-1] == (1, 1):
            if not any(v['list'] == p_list for v in valid_paths):
                valid_paths.append({'dict': p_dict, 'list': p_list})

    print(f"\nExtracted {len(valid_paths)} unique valid paths from final population.")

    if not valid_paths:
        print("GA failed to find a valid path to the goal. You might need to run it again or check mutation settings.")
        return

    for path_data in valid_paths:
        t, c = evaluate_path(path_data['list'], time_zones, cost_zones)
        path_data['time'] = t
        path_data['cost'] = c
        path_data['balanced'] = t + c

    fastest = min(valid_paths, key=lambda x: x['time'])
    cheapest = min(valid_paths, key=lambda x: x['cost'])
    balanced = min(valid_paths, key=lambda x: x['balanced'])

    print("\n--- Extracted Solutions from A SINGLE Evolution ---")
    print(f"[Green] Fastest Path  - Time: {fastest['time']:<5} | Cost: {fastest['cost']}")
    print(f"[Cyan]  Cheapest Path - Time: {cheapest['time']:<5} | Cost: {cheapest['cost']}")
    print(f"[Red]   Balanced Path - Time: {balanced['time']:<5} | Cost: {balanced['cost']}")

    a_fast = agent(m, color="green", filled=True, footprints=True)
    a_cheap = agent(m, color="cyan", filled=True, footprints=True)
    a_balanced = agent(m, color="red", filled=True, footprints=True)

    m.tracePath({a_fast: fastest['dict'], a_cheap: cheapest['dict'], a_balanced: balanced['dict']}, delay=100)

    # Start plot window in a separate process so it can run alongside pyamaze.
    plot_process = mp.Process(target=plot_path_comparison, args=(fastest, cheapest, balanced), daemon=True)
    plot_process.start()

    try:
        m.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        if plot_process.is_alive():
            plot_process.join(timeout=0.5)
        if plot_process.is_alive():
            plot_process.terminate()
            plot_process.join(timeout=1)


if __name__ == '__main__':
    mp.freeze_support()
    main()
    sys.exit(0)