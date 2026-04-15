import os
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

from pyamaze import maze, agent
from utils import to_path, move
from maze_definition import CostMaze
from ga_multi_objective import run_ga_multi_objective
from solution_extraction import extract_pareto_solutions, print_solution_comparison
from multi_run_analysis import run_multiple_ga_experiments, compare_experiments
from visualization import visualize_solutions, plot_convergence, create_comparison_plot, animate_solve

MAZE_ROWS = 8
MAZE_COLS = 8

# ============================================================================
# STEP 1 & 2: Create maze with costs
# ============================================================================
print("STEP 1-2: Defining Maze with Cost Regions...")
print("-" * 60)

m = maze(MAZE_ROWS, MAZE_COLS)
m.CreateMaze(loopPercent=100)  # loopPercent=100 ensures multiple alternative paths exist!

cost_maze = CostMaze(MAZE_ROWS, MAZE_COLS)
cost_maze.maze_map = m.maze_map
cost_maze.maze_structure = m.maze_map
cost_maze.define_regions()

print(f"  Maze created with size: {MAZE_ROWS}x{MAZE_COLS}")
print("  Cost regions defined:")
print("  - Swamp: slow x5, cheap x0.5")
print("  - Highway: fast x0.5, expensive x3")
print("  - Mountain: medium speed, costly")

# ============================================================================
# STEP 3-5: Run Multi-Objective GA
# ============================================================================
print("\n\nSTEP 3-5: Running Multi-Objective GA with Different alpha Values...")
print("-" * 60)

experiments = run_multiple_ga_experiments(
    cost_maze,
    alpha_values=[0.0, 0.5, 1.0]
)

# ============================================================================
# STEP 6: Visualize - save animations as GIF + static PNGs
# ============================================================================
print("\n\nSTEP 6: Generating Visualizations...")
print("-" * 60)

gif_files = []
for alpha in [0.0, 0.5, 1.0]:
    solutions = experiments[alpha]['solutions']

    print(f"\n  Processing alpha={alpha}...")
    gif = animate_solve(cost_maze, solutions, alpha=alpha, speed_ms=100)
    gif_files.append(gif)

    visualize_solutions(cost_maze, solutions)
    plot_convergence(experiments[alpha]['ga_history'], alpha)

# ============================================================================
# STEP 7: Cross-Experiment Comparison
# ============================================================================
print("\n\nSTEP 7: Comparing Across All Experiments...")
print("-" * 60)

compare_experiments(experiments)
create_comparison_plot(experiments)

# ============================================================================
# Done - open output folder
# ============================================================================
output_dir = os.path.join(os.path.dirname(__file__), 'output')
print("\n" + "=" * 80)
print("ALL DONE!")
print("=" * 80)
print(f"\nAll outputs saved to: {os.path.abspath(output_dir)}")
print("\nGenerated files:")
for f in os.listdir(output_dir):
    fpath = os.path.join(output_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  - {f}  ({size_kb:.1f} KB)")

print("\nOpening output folder...")
os.startfile(os.path.abspath(output_dir))