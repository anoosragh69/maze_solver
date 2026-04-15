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
    print("OVERALL OPTIMAL ROUTES DISCOVERED")
    print("="*80)
    
    # Extract the absolute best path found by each priority run
    # Since elitism converges heavily, the fastest/cheapest in a run are the same.
    opt_time = experiments[0.0]['solutions']['fastest']
    opt_balanced = experiments[0.5]['solutions']['balanced']
    opt_cost = experiments[1.0]['solutions']['cheapest']
    
    print("\n1. FASTEST ROUTE (Time Priority)")
    print(f"   Time Taken:  {opt_time['time']:.2f}")
    print(f"   Money Cost:  {opt_time['cost']:.2f}")
    print(f"   True Length: {opt_time['path_length']} moves")
    
    print("\n2. BALANCED ROUTE (Equal Priority)")
    print(f"   Time Taken:  {opt_balanced['time']:.2f}")
    print(f"   Money Cost:  {opt_balanced['cost']:.2f}")
    print(f"   True Length: {opt_balanced['path_length']} moves")
    
    print("\n3. CHEAPEST ROUTE (Cost Priority)")
    print(f"   Time Taken:  {opt_cost['time']:.2f}")
    print(f"   Money Cost:  {opt_cost['cost']:.2f}")
    print(f"   True Length: {opt_cost['path_length']} moves")
    
    print("\n" + "-"*80)
    print("Trade-off Summary:")
    print(f"  By choosing FASTEST over CHEAPEST, you save "
          f"{opt_cost['time'] - opt_time['time']:.2f} Time, "
          f"but pay {opt_time['cost'] - opt_cost['cost']:.2f} extra Cost.")
    print("="*80 + "\n")