from utils import move
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — no blocking windows
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patheffects as pe
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Color palette ---
BG_COLOR       = '#0f0f1a'
WALL_COLOR     = '#c0c0d0'
PATH_COLORS    = {'fastest': '#00e5ff', 'cheapest': '#76ff03', 'balanced': '#ff6e40'}
START_COLOR    = '#ffea00'
GOAL_COLOR     = '#ff1744'
REGION_CMAPS   = {
    'swamp':    ('#1b5e20', 0.35),
    'highway':  ('#e65100', 0.30),
    'mountain': ('#4a148c', 0.30),
    'default':  ('#1a237e', 0.15),
}


def _trace_path(maze_obj, moves):
    """Return list of (row, col) positions the path visits."""
    pos = (maze_obj.rows, maze_obj.cols)
    goal = (1, 1)
    path = [pos]
    for d in moves:
        if pos in maze_obj.maze_map and maze_obj.maze_map[pos][d] == 1:
            pos = move(pos, d)
            path.append(pos)
            if pos == goal:
                break
    return path


def _draw_maze(ax, maze_obj, cell_size=1):
    """Draw proper maze walls and color-coded regions."""
    rows, cols = maze_obj.rows, maze_obj.cols

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            x = (c - 1) * cell_size
            y = (rows - r) * cell_size

            tc = maze_obj.time_cost[r, c] if r < maze_obj.time_cost.shape[0] and c < maze_obj.time_cost.shape[1] else 1
            if tc >= 4:
                color, alpha = REGION_CMAPS['swamp']
            elif tc <= 0.6:
                color, alpha = REGION_CMAPS['highway']
            elif tc >= 1.5:
                color, alpha = REGION_CMAPS['mountain']
            else:
                color, alpha = REGION_CMAPS['default']

            rect = Rectangle((x, y), cell_size, cell_size,
                              facecolor=color, alpha=alpha, edgecolor='none')
            ax.add_patch(rect)

    wall_lw = 2.0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            cell = (r, c)
            if cell not in maze_obj.maze_map:
                continue
            x = (c - 1) * cell_size
            y = (rows - r) * cell_size
            walls = maze_obj.maze_map[cell]
            if walls.get('N', 0) == 0:
                ax.plot([x, x + cell_size], [y + cell_size, y + cell_size],
                        color=WALL_COLOR, lw=wall_lw, solid_capstyle='round')
            if walls.get('S', 0) == 0:
                ax.plot([x, x + cell_size], [y, y],
                        color=WALL_COLOR, lw=wall_lw, solid_capstyle='round')
            if walls.get('E', 0) == 0:
                ax.plot([x + cell_size, x + cell_size], [y, y + cell_size],
                        color=WALL_COLOR, lw=wall_lw, solid_capstyle='round')
            if walls.get('W', 0) == 0:
                ax.plot([x, x], [y, y + cell_size],
                        color=WALL_COLOR, lw=wall_lw, solid_capstyle='round')

    # Outer border
    ax.plot([0, cols * cell_size], [0, 0], color=WALL_COLOR, lw=3)
    ax.plot([0, cols * cell_size], [rows * cell_size, rows * cell_size], color=WALL_COLOR, lw=3)
    ax.plot([0, 0], [0, rows * cell_size], color=WALL_COLOR, lw=3)
    ax.plot([cols * cell_size, cols * cell_size], [0, rows * cell_size], color=WALL_COLOR, lw=3)

    ax.set_xlim(-0.1, cols * cell_size + 0.1)
    ax.set_ylim(-0.1, rows * cell_size + 0.1)
    ax.set_aspect('equal')
    ax.axis('off')


def _cell_to_xy(r, c, rows, cell_size=1):
    x = (c - 1) * cell_size + cell_size / 2
    y = (rows - r) * cell_size + cell_size / 2
    return x, y


# =============================================================================
# Animate the solve and save as GIF
# =============================================================================
def animate_solve(maze_obj, solutions, alpha=0.5, speed_ms=100):
    """Save a GIF animation of the maze being solved step-by-step."""
    rows, cols = maze_obj.rows, maze_obj.cols
    keys = ['fastest', 'cheapest', 'balanced']

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=BG_COLOR)
    fig.suptitle(f'Real-Time Maze Solving  (a = {alpha})',
                 color='white', fontsize=16, fontweight='bold', y=0.97)

    paths = {}
    lines = {}
    dots  = {}

    for idx, key in enumerate(keys):
        ax = axes[idx]
        ax.set_facecolor(BG_COLOR)
        _draw_maze(ax, maze_obj)

        # Start / Goal markers
        sx, sy = _cell_to_xy(rows, cols, rows)
        gx, gy = _cell_to_xy(1, 1, rows)
        ax.plot(sx, sy, 'o', color=START_COLOR, markersize=14, zorder=5,
                markeredgecolor='white', markeredgewidth=1.5)
        ax.text(sx, sy - 0.35, 'S', color=START_COLOR, fontsize=8,
                ha='center', va='top', fontweight='bold')
        ax.plot(gx, gy, '*', color=GOAL_COLOR, markersize=18, zorder=5,
                markeredgecolor='white', markeredgewidth=1)
        ax.text(gx, gy - 0.35, 'G', color=GOAL_COLOR, fontsize=8,
                ha='center', va='top', fontweight='bold')

        sol = solutions[key]
        path = _trace_path(maze_obj, sol['moves'])
        paths[key] = path

        color = PATH_COLORS[key]
        line, = ax.plot([], [], color=color, lw=3, solid_capstyle='round',
                        path_effects=[pe.Stroke(linewidth=5, foreground='black'), pe.Normal()],
                        zorder=4)
        dot, = ax.plot([], [], 'o', color=color, markersize=8, zorder=6,
                       markeredgecolor='white', markeredgewidth=1.5)
        lines[key] = line
        dots[key]  = dot

        ax.set_title(f"{sol['label']}\nTime: {sol['time']:.1f}  |  Cost: {sol['cost']:.1f}",
                     color='white', fontsize=10, fontweight='bold', pad=8)

    max_len = max(len(p) for p in paths.values())

    def _update(frame):
        artists = []
        for key in keys:
            p = paths[key]
            n = min(frame + 1, len(p))
            xs = [_cell_to_xy(r, c, rows)[0] for r, c in p[:n]]
            ys = [_cell_to_xy(r, c, rows)[1] for r, c in p[:n]]
            lines[key].set_data(xs, ys)
            if xs:
                dots[key].set_data([xs[-1]], [ys[-1]])
            artists.extend([lines[key], dots[key]])
        return artists

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    # Save as GIF
    ani = animation.FuncAnimation(fig, _update, frames=max_len + 5,
                                  interval=speed_ms, blit=True, repeat=False)
    gif_path = os.path.join(OUTPUT_DIR, f'maze_solve_a{alpha}.gif')
    ani.save(gif_path, writer='pillow', fps=10, dpi=100)
    plt.close(fig)
    print(f"  [OK] Saved animation: {gif_path}")
    return gif_path


# =============================================================================
# Static comparison
# =============================================================================
def visualize_solutions(maze_obj, solutions):
    """Draw all three solution paths side-by-side with proper maze walls."""
    rows, cols = maze_obj.rows, maze_obj.cols
    keys = ['fastest', 'cheapest', 'balanced']

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=BG_COLOR)
    fig.suptitle('Solution Comparison', color='white', fontsize=16,
                 fontweight='bold', y=0.97)

    for idx, key in enumerate(keys):
        ax = axes[idx]
        ax.set_facecolor(BG_COLOR)
        _draw_maze(ax, maze_obj)

        sol = solutions[key]
        path = _trace_path(maze_obj, sol['moves'])

        color = PATH_COLORS[key]
        xs = [_cell_to_xy(r, c, rows)[0] for r, c in path]
        ys = [_cell_to_xy(r, c, rows)[1] for r, c in path]
        ax.plot(xs, ys, color=color, lw=3, solid_capstyle='round',
                path_effects=[pe.Stroke(linewidth=5, foreground='black'), pe.Normal()],
                zorder=4, label='Path')
        if xs:
            ax.plot(xs[-1], ys[-1], 'o', color=color, markersize=8, zorder=6,
                    markeredgecolor='white', markeredgewidth=1.5)

        sx, sy = _cell_to_xy(rows, cols, rows)
        gx, gy = _cell_to_xy(1, 1, rows)
        ax.plot(sx, sy, 'o', color=START_COLOR, markersize=14, zorder=5,
                markeredgecolor='white', markeredgewidth=1.5, label='Start')
        ax.plot(gx, gy, '*', color=GOAL_COLOR, markersize=18, zorder=5,
                markeredgecolor='white', markeredgewidth=1, label='Goal')

        ax.set_title(f"{sol['label']}\nTime: {sol['time']:.1f}  |  Cost: {sol['cost']:.1f}",
                     color='white', fontsize=10, fontweight='bold', pad=8)
        ax.legend(loc='lower right', fontsize=7, framealpha=0.5,
                  facecolor='#222', edgecolor='#555', labelcolor='white')

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    png_path = os.path.join(OUTPUT_DIR, 'solution_comparison.png')
    plt.savefig(png_path, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {png_path}")


# =============================================================================
# Convergence plot (FIXED - accepts GAState)
# =============================================================================
def plot_convergence(ga_state, alpha):
    """Plot GA convergence over generations."""
    history = ga_state.generation_history
    generations = len(history)

    best_fitness = []
    avg_fitness  = []

    for gen_scores in history:
        fitnesses = [s['fitness'] for s in gen_scores]
        best_fitness.append(min(fitnesses))
        avg_fitness.append(sum(fitnesses) / len(fitnesses))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), facecolor=BG_COLOR)

    ax1.set_facecolor('#141422')
    ax1.plot(best_fitness, color='#00e5ff', linewidth=2.5, label='Best Fitness',
             path_effects=[pe.Stroke(linewidth=4, foreground='#004d5a'), pe.Normal()])
    ax1.plot(avg_fitness, color='#ff6e40', linewidth=2, linestyle='--', label='Avg Fitness')
    ax1.fill_between(range(generations), best_fitness, avg_fitness,
                     color='#00e5ff', alpha=0.08)
    ax1.set_xlabel('Generation', color='white')
    ax1.set_ylabel('Fitness Score', color='white')
    ax1.set_title(f'GA Convergence  (a = {alpha})', color='white', fontweight='bold')
    ax1.legend(facecolor='#222', edgecolor='#555', labelcolor='white')
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.15, color='white')
    for spine in ax1.spines.values():
        spine.set_color('#333')

    ax2.set_facecolor('#141422')
    last_gen = history[-1]
    times = [s['time'] for s in last_gen]
    costs = [s['cost'] for s in last_gen]
    ax2.scatter(times, costs, c='#76ff03', alpha=0.7, s=60, edgecolors='white',
                linewidths=0.5, zorder=3)
    ax2.set_xlabel('Total Time', color='white')
    ax2.set_ylabel('Total Cost', color='white')
    ax2.set_title(f'Final Population Trade-off  (a = {alpha})', color='white', fontweight='bold')
    ax2.tick_params(colors='white')
    ax2.grid(True, alpha=0.15, color='white')
    for spine in ax2.spines.values():
        spine.set_color('#333')

    plt.tight_layout()
    fname = os.path.join(OUTPUT_DIR, f'convergence_a{alpha}.png')
    plt.savefig(fname, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {fname}")


# =============================================================================
# Cross-experiment comparison
# =============================================================================
def create_comparison_plot(experiments):
    """Create comparison plots across all alpha values."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), facecolor=BG_COLOR)
    fig.suptitle('Cross-Experiment Analysis', color='white', fontsize=16,
                 fontweight='bold', y=0.98)

    alphas = sorted(experiments.keys())
    palette = ['#00e5ff', '#76ff03', '#ff6e40']

    def _style_ax(ax, title, xlabel, ylabel):
        ax.set_facecolor('#141422')
        ax.set_title(title, color='white', fontweight='bold', fontsize=11)
        ax.set_xlabel(xlabel, color='white')
        ax.set_ylabel(ylabel, color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.15, color='white')
        for s in ax.spines.values():
            s.set_color('#333')

    ax = axes[0, 0]
    times = [experiments[a]['solutions']['fastest']['time'] for a in alphas]
    costs = [experiments[a]['solutions']['fastest']['cost'] for a in alphas]
    ax.plot(alphas, times, 'o-', color='#00e5ff', label='Time', lw=2.5)
    ax.plot(alphas, costs, 's-', color='#ff6e40', label='Cost', lw=2.5)
    _style_ax(ax, 'Fastest Paths: Time vs Cost', 'a', 'Value')
    ax.legend(facecolor='#222', edgecolor='#555', labelcolor='white')

    ax = axes[0, 1]
    times = [experiments[a]['solutions']['cheapest']['time'] for a in alphas]
    costs = [experiments[a]['solutions']['cheapest']['cost'] for a in alphas]
    ax.plot(alphas, times, 'o-', color='#00e5ff', label='Time', lw=2.5)
    ax.plot(alphas, costs, 's-', color='#ff6e40', label='Cost', lw=2.5)
    _style_ax(ax, 'Cheapest Paths: Time vs Cost', 'a', 'Value')
    ax.legend(facecolor='#222', edgecolor='#555', labelcolor='white')

    ax = axes[1, 0]
    for i, key in enumerate(['fastest', 'cheapest', 'balanced']):
        vals = [experiments[a]['solutions'][key]['fitness'] for a in alphas]
        ax.plot(alphas, vals, 'o-', color=palette[i], label=key.title(), lw=2.5)
    _style_ax(ax, 'Solution Fitness Across a', 'a', 'Fitness')
    ax.legend(facecolor='#222', edgecolor='#555', labelcolor='white')

    ax = axes[1, 1]
    markers = {'fastest': 'o', 'cheapest': 's', 'balanced': '^'}
    for a_idx, alpha in enumerate(alphas):
        for ki, key in enumerate(['fastest', 'cheapest', 'balanced']):
            sol = experiments[alpha]['solutions'][key]
            ax.scatter(sol['time'], sol['cost'], color=palette[ki], s=120,
                       marker=markers[key], edgecolors='white', linewidths=0.8,
                       zorder=3, label=f'{key.title()}' if a_idx == 0 else '')
    _style_ax(ax, 'Pareto Front: Trade-off', 'Time', 'Cost')
    ax.legend(facecolor='#222', edgecolor='#555', labelcolor='white')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    fname = os.path.join(OUTPUT_DIR, 'cross_experiment_analysis.png')
    plt.savefig(fname, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  [OK] Saved: {fname}")