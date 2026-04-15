from ga_multi_objective import run_ga_multi_objective
from solution_extraction import extract_pareto_solutions, print_solution_comparison
from visualization import visualize_solutions, plot_convergence, create_comparison_plot
def run_multiple_ga_experiments(maze_obj, alpha_values=[0.0, 0.5, 1.0]):
    """
    Run GA multiple times with different objective weights
    
    Args:
        maze_obj: CostMaze object
        alpha_values: list of α values to test
    
    Returns:
        experiments: dict of results per α value
    """
    
    experiments = {}
    
    for alpha in alpha_values:
        print(f"\n\nRUNNING EXPERIMENT WITH α={alpha}")
        print("This determines: (1-α)×Time + α×Cost")
        
        final_pop, ga_history = run_ga_multi_objective(
            maze_obj,
            generations=50,
            population_size=20,
            alpha=alpha
        )
        
        solutions = extract_pareto_solutions(final_pop)
        print_solution_comparison(solutions)
        
        experiments[alpha] = {
            'final_population': final_pop,
            'ga_history': ga_history,
            'solutions': solutions
        }
    
    return experiments

def compare_experiments(experiments):
    """Compare results across different α values"""
    
    print("\n" + "="*80)
    print("CROSS-EXPERIMENT ANALYSIS")
    print("="*80)
    
    print("\nFastest Paths by α-value:")
    print(f"{'α':>6} | {'Time':>8} | {'Cost':>8} | {'Fitness':>8}")
    print("-" * 40)
    
    for alpha in sorted(experiments.keys()):
        fastest = experiments[alpha]['solutions']['fastest']
        print(f"{alpha:>6.1f} | {fastest['time']:>8.2f} | {fastest['cost']:>8.2f} | {fastest['fitness']:>8.2f}")
    
    print("\nCheapest Paths by α-value:")
    print(f"{'α':>6} | {'Time':>8} | {'Cost':>8} | {'Fitness':>8}")
    print("-" * 40)
    
    for alpha in sorted(experiments.keys()):
        cheapest = experiments[alpha]['solutions']['cheapest']
        print(f"{alpha:>6.1f} | {cheapest['time']:>8.2f} | {cheapest['cost']:>8.2f} | {cheapest['fitness']:>8.2f}")
    
    print("\n" + "="*80 + "\n")