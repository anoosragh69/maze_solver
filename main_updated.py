from pyamaze import maze, agent
from utils import to_path, move
from maze_definition import CostMaze
from ga_multi_objective import run_ga_multi_objective
from solution_extraction import extract_pareto_solutions, print_solution_comparison
from multi_run_analysis import run_multiple_ga_experiments, compare_experiments
from visualization import visualize_solutions, plot_convergence, create_comparison_plot

# ============================================================================
# STEP 1 & 2: Create maze with costs
# ============================================================================
print("STEP 1-2: Defining Maze with Cost Regions...")
print("-" * 60)

# Create base maze using pyamaze
m = maze(5, 5)
m.CreateMaze()

# Extend with costs
cost_maze = CostMaze(5, 5)
cost_maze.maze_map = m.maze_map
cost_maze.maze_structure = m.maze_map
cost_maze.define_regions()

print("✓ Maze created with size: 5x5")
print("✓ Cost regions defined:")
print("  - Swamp (rows 2-4, cols 2-4): slow×5, cheap×0.5")
print("  - Highway (rows 3-5, cols 4-6): fast×0.5, expensive×3")
print("  - Mountain (rows 1-3, cols 4-6): medium")

# ============================================================================
# STEP 3-5: Run Multi-Objective GA
# ============================================================================
print("\n\nSTEP 3-5: Running Multi-Objective GA with Different α Values...")
print("-" * 60)

experiments = run_multiple_ga_experiments(
    cost_maze,
    alpha_values=[0.0, 0.5, 1.0]  # Time-priority, Balanced, Cost-priority
)

# ============================================================================
# STEP 6: Visualize Solutions
# ============================================================================
print("\n\nSTEP 6: Visualizing Solutions...")
print("-" * 60)

for alpha in [0.0, 0.5, 1.0]:
    solutions = experiments[alpha]['solutions']
    print(f"\nVisualizing solutions for α={alpha}...")
    visualize_solutions(cost_maze, solutions)
    plot_convergence(experiments[alpha]['ga_history'], alpha)

# ============================================================================
# STEP 7: Cross-Experiment Comparison
# ============================================================================
print("\n\nSTEP 7: Comparing Across All Experiments...")
print("-" * 60)

compare_experiments(experiments)
create_comparison_plot(experiments)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("""
This demonstration shows how a single GA framework can solve multi-objective
optimization by:

1. ✓ Defining regions with time and cost trade-offs
2. ✓ Creating a flexible fitness function with α parameter
3. ✓ Running the GA once per objective priority
4. ✓ Extracting distinct solutions (fastest, cheapest, balanced)
5. ✓ Visualizing the trade-offs and convergence behavior
6. ✓ Comparing results across different priorities

Key Insight: By varying α, we show that a SINGLE GA design can serve
multiple real-world objectives without modification to the core algorithm.
The parameter α simply weights the objectives differently.
""")
print("="*80)