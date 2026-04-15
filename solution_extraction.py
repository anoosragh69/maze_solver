def extract_pareto_solutions(final_population):
    """
    Extract meaningful solutions from final population
    
    Returns:
        solutions: dict with 'fastest', 'cheapest', 'balanced'
    """
    
    # Sort by different metrics
    by_time = sorted(final_population, key=lambda x: x['time'])
    by_cost = sorted(final_population, key=lambda x: x['cost'])
    by_fitness = sorted(final_population, key=lambda x: x['fitness'])
    
    solutions = {
        'fastest': {
            'moves': by_time[0]['moves'],
            'time': by_time[0]['time'],
            'cost': by_time[0]['cost'],
            'fitness': by_time[0]['fitness'],
            'path_length': by_time[0].get('path_length', len(by_time[0]['moves'])),
            'label': 'Time-Optimized (Fastest)'
        },
        'cheapest': {
            'moves': by_cost[0]['moves'],
            'time': by_cost[0]['time'],
            'cost': by_cost[0]['cost'],
            'fitness': by_cost[0]['fitness'],
            'path_length': by_cost[0].get('path_length', len(by_cost[0]['moves'])),
            'label': 'Cost-Optimized (Cheapest)'
        },
        'balanced': {
            'moves': by_fitness[0]['moves'],
            'time': by_fitness[0]['time'],
            'cost': by_fitness[0]['cost'],
            'fitness': by_fitness[0]['fitness'],
            'path_length': by_fitness[0].get('path_length', len(by_fitness[0]['moves'])),
            'label': 'Balanced (Best Fitness)'
        }
    }
    
    return solutions

def print_solution_comparison(solutions):
    """Pretty-print comparison of solutions"""
    
    print("\n" + "="*80)
    print("SOLUTION COMPARISON")
    print("="*80)
    
    for key, solution in solutions.items():
        print(f"\n{solution['label']}:")
        print(f"  Time Cost:     {solution['time']:.2f}")
        print(f"  Money Cost:    {solution['cost']:.2f}")
        print(f"  Combined Fitness: {solution['fitness']:.2f}")
        print(f"  Path Length:   {solution.get('path_length', len(solution['moves']))} moves")
    
    # Calculate trade-offs
    fastest_cost = solutions['fastest']['cost']
    cheapest_time = solutions['cheapest']['time']
    
    print(f"\nTrade-off Analysis:")
    print(f"  By choosing FASTEST over CHEAPEST:")
    print(f"    - Saves {solutions['cheapest']['time'] - solutions['fastest']['time']:.2f} time units")
    print(f"    - Costs {solutions['fastest']['cost'] - fastest_cost:.2f} additional money")
    
    print(f"  By choosing CHEAPEST over FASTEST:")
    print(f"    - Saves {solutions['fastest']['cost'] - solutions['cheapest']['cost']:.2f} money")
    print(f"    - Takes {solutions['cheapest']['time'] - solutions['fastest']['time']:.2f} additional time")
    
    print("\n" + "="*80 + "\n")