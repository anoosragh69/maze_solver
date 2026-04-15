from pyamaze import maze, agent
from utils import to_path, generate_penalty_zones, evaluate_path
from ga import run_ga

# --- 1. create maze and zones ---
rows, cols = 10, 10
print(f"Creating a {rows}x{cols} maze...")
m = maze(rows, cols)
m.CreateMaze(loopPercent=100) # adding massive loops to allow many diverse valid paths

time_zones, cost_zones = generate_penalty_zones(rows, cols, time_prob=0.3, cost_prob=0.3)

# Note: Since PyAmaze doesn't support custom colored cells arbitrarily by default,
# visualizing the zones itself is limited, but we track and evaluate against them properly.

# --- 2. run single GA evolution ---
print("Running GA to learn valid path population...")
population = run_ga(m, generations=150, population_size=400)

# --- 3. extract valid paths ---
valid_paths = []
for chrom in population:
    p_dict, p_list = to_path(chrom, m)
    # Check if path reaches the goal (1, 1)
    if p_list[-1] == (1, 1):
        # Optional: eliminate exact duplicate paths
        if not any(v['list'] == p_list for v in valid_paths):
            valid_paths.append({'dict': p_dict, 'list': p_list})

print(f"\nExtracted {len(valid_paths)} unique valid paths from final population.")

if not valid_paths:
    print("GA failed to find a valid path to the goal. You might need to run it again or check mutation settings.")
    import sys
    sys.exit()

# --- 4. evaluate valid paths ---
for idx, path_data in enumerate(valid_paths):
    t, c = evaluate_path(path_data['list'], time_zones, cost_zones)
    path_data['time'] = t
    path_data['cost'] = c
    path_data['balanced'] = t + c

# --- 5. extract best multi-objective paths ---
fastest = min(valid_paths, key=lambda x: x['time'])
cheapest = min(valid_paths, key=lambda x: x['cost'])
balanced = min(valid_paths, key=lambda x: x['balanced'])

print("\n--- Extracted Solutions from A SINGLE Evolution ---")
print(f"[Green] Fastest Path  - Time: {fastest['time']:<5} | Cost: {fastest['cost']}")
print(f"[Cyan]  Cheapest Path - Time: {cheapest['time']:<5} | Cost: {cheapest['cost']}")
print(f"[Red]   Balanced Path - Time: {balanced['time']:<5} | Cost: {balanced['cost']}")

# --- 6. setup maze visualizer agents ---
# Fastest: Green
a_fast = agent(m, color="green", filled=True, footprints=True)
# Cheapest: Cyan
a_cheap = agent(m, color="cyan", filled=True, footprints=True)
# Balanced: Red
a_balanced = agent(m, color="red", filled=True, footprints=True)

# Add delay=100 to actually see the paths trace easily
m.tracePath({a_fast: fastest['dict'], a_cheap: cheapest['dict'], a_balanced: balanced['dict']}, delay=100)

print("\nOpening UI. Close the pyamaze window to exit.")
m.run()