from fitness_function import calculate_path_metrics, combined_fitness
import random
from utils import move

class GAState:
    """Tracks GA state and history for analysis"""
    
    def __init__(self):
        self.generation_history = []  # Each gen: [individuals with metrics]
        self.best_per_generation = []  # Track best individual per gen

def generate_valid_moves(m, steps=20):
    """Keep existing implementation"""
    pos = (m.rows, m.cols)
    moves = []
    
    for _ in range(steps):
        valid_dirs = [d for d in 'ESNW' if m.maze_map[pos][d] == 1]
        if not valid_dirs:
            break
        d = random.choice(valid_dirs)
        moves.append(d)
        pos = move(pos, d)
    
    return moves

def crossover(parents, population_size=20):
    """Keep existing implementation"""
    children = []
    
    for _ in range(population_size):
        p1 = random.choice(parents)
        p2 = random.choice(parents)
        
        cut = random.randint(1, min(len(p1), len(p2)) - 1)
        child = p1[:cut] + p2[cut:]
        children.append(child)
    
    return children

def mutate(population, rate=0.2):
    """Keep existing implementation"""
    moves = ['N', 'S', 'E', 'W']
    
    for chrom in population:
        if random.random() < rate:
            idx = random.randint(0, len(chrom) - 1)
            chrom[idx] = random.choice(moves)
    
    return population

def run_ga_multi_objective(maze_obj, generations=50, population_size=20, alpha=0.5):
    """
    Run GA with multi-objective fitness
    
    Args:
        maze_obj: CostMaze object with time/cost maps
        generations: number of generations to evolve
        population_size: size of population per generation
        alpha: weight for cost in fitness (0.0 = time, 1.0 = cost)
    
    Returns:
        final_population: list of (moves, time, cost, fitness)
        ga_history: complete history for analysis
    """
    
    # Initialize population
    population = [generate_valid_moves(maze_obj, steps=40) for _ in range(population_size)]
    
    ga_state = GAState()
    
    print(f"\n{'='*60}")
    print(f"GA Multi-Objective Optimization (α={alpha})")
    print(f"{'='*60}")
    
    for gen in range(generations):
        # Evaluate fitness for all individuals
        scores = []
        for moves in population:
            fitness_val, time_val, cost_val = combined_fitness(
                moves, maze_obj, alpha=alpha
            )
            scores.append({
                'moves': moves,
                'fitness': fitness_val,
                'time': time_val,
                'cost': cost_val
            })
        
        # Sort by fitness (lower is better)
        scores.sort(key=lambda x: x['fitness'])
        
        # Store generation history
        ga_state.generation_history.append(scores)
        ga_state.best_per_generation.append(scores[0])
        
        # Print progress
        best = scores[0]
        if gen % 10 == 0:
            print(f"Gen {gen:3d} | Best Fitness: {best['fitness']:8.2f} | "
                  f"Time: {best['time']:8.2f} | Cost: {best['cost']:8.2f}")
        
        # Selection: keep top performers
        top_performers = [s['moves'] for s in scores[:5]]
        
        # Crossover
        children = crossover(top_performers, population_size)
        
        # Mutation
        population = mutate(children, rate=0.2)
    
    # Final evaluation
    final_scores = []
    for moves in population:
        fitness_val, time_val, cost_val = combined_fitness(
            moves, maze_obj, alpha=alpha
        )
        final_scores.append({
            'moves': moves,
            'fitness': fitness_val,
            'time': time_val,
            'cost': cost_val
        })
    
    final_scores.sort(key=lambda x: x['fitness'])
    
    print(f"\nFinal Population Statistics (α={alpha}):")
    print(f"  Best Fitness: {final_scores[0]['fitness']:.2f}")
    print(f"  Avg Fitness: {sum(s['fitness'] for s in final_scores) / len(final_scores):.2f}")
    print(f"  Worst Fitness: {final_scores[-1]['fitness']:.2f}")
    print(f"{'='*60}\n")
    
    return final_scores, ga_state