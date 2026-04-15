from utils import move
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def visualize_solutions(maze_obj, solutions):
    """Visualize all three solutions side by side"""
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    solution_keys = ['fastest', 'cheapest', 'balanced']
    colors_map = {'fastest': 'blue', 'cheapest': 'green', 'balanced': 'red'}
    
    for idx, key in enumerate(solution_keys):
        ax = axes[idx]
        solution = solutions[key]
        
        # Draw cost map as heatmap
        im = ax.imshow(maze_obj.money_cost, cmap='YlOrRd', alpha=0.3)
        
        # Draw maze structure (walls)
        # (Simplified - you can enhance this)
        
        # Draw path
        pos = (maze_obj.rows, maze_obj.cols)
        path_x, path_y = [maze_obj.cols], [maze_obj.rows]
        
        for direction in solution['moves']:
            if maze_obj.maze_map[pos][direction] == 1:
                pos = move(pos, direction)
                path_y.append(pos[0])
                path_x.append(pos[1])
        
        ax.plot(path_x, path_y, color=colors_map[key], linewidth=2, marker='o', 
                markersize=4, label='Path')
        
        # Mark start and goal
        ax.plot(maze_obj.cols, maze_obj.rows, 'gs', markersize=12, label='Start')
        ax.plot(1, 1, 'r*', markersize=15, label='Goal')
        
        # Title and labels
        ax.set_title(f"{solution['label']}\n"
                     f"Time: {solution['time']:.2f} | Cost: {solution['cost']:.2f}",
                     fontsize=11, fontweight='bold')
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('solution_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: solution_comparison.png")
    plt.show()

def plot_convergence(ga_history, alpha):
    """Plot GA convergence over generations"""
    
    generations = len(ga_history)
    best_fitness = []
    avg_fitness = []
    
    for gen_scores in ga_history:
        fitnesses = [s['fitness'] for s in gen_scores]
        best_fitness.append(min(fitnesses))
        avg_fitness.append(sum(fitnesses) / len(fitnesses))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Fitness convergence
    ax1.plot(best_fitness, 'b-', linewidth=2, label='Best Fitness')
    ax1.plot(avg_fitness, 'r--', linewidth=2, label='Avg Fitness')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Fitness Score')
    ax1.set_title(f'GA Convergence (α={alpha})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Time vs Cost scatter in final population
    last_gen = ga_history[-1]
    times = [s['time'] for s in last_gen]
    costs = [s['cost'] for s in last_gen]
    
    ax2.scatter(times, costs, alpha=0.6, s=50)
    ax2.set_xlabel('Total Time')
    ax2.set_ylabel('Total Cost')
    ax2.set_title(f'Final Population Trade-off (α={alpha})')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'convergence_alpha_{alpha}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: convergence_alpha_{alpha}.png")
    plt.show()

def create_comparison_plot(experiments):
    """Create comparison plots across all α values"""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    alphas = sorted(experiments.keys())
    
    # Plot 1: Fastest paths across α
    ax = axes[0, 0]
    times = [experiments[a]['solutions']['fastest']['time'] for a in alphas]
    costs = [experiments[a]['solutions']['fastest']['cost'] for a in alphas]
    ax.plot(alphas, times, 'b-o', label='Time', linewidth=2)
    ax.plot(alphas, costs, 'r-s', label='Cost', linewidth=2)
    ax.set_xlabel('α (0=time priority, 1=cost priority)')
    ax.set_ylabel('Value')
    ax.set_title('Fastest Paths: Time vs Cost')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Cheapest paths across α
    ax = axes[0, 1]
    times = [experiments[a]['solutions']['cheapest']['time'] for a in alphas]
    costs = [experiments[a]['solutions']['cheapest']['cost'] for a in alphas]
    ax.plot(alphas, times, 'b-o', label='Time', linewidth=2)
    ax.plot(alphas, costs, 'r-s', label='Cost', linewidth=2)
    ax.set_xlabel('α (0=time priority, 1=cost priority)')
    ax.set_ylabel('Value')
    ax.set_title('Cheapest Paths: Time vs Cost')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Fitness values
    ax = axes[1, 0]
    for key in ['fastest', 'cheapest', 'balanced']:
        fitness_vals = [experiments[a]['solutions'][key]['fitness'] for a in alphas]
        ax.plot(alphas, fitness_vals, marker='o', label=key.title(), linewidth=2)
    ax.set_xlabel('α')
    ax.set_ylabel('Fitness')
    ax.set_title('Solution Fitness Across α Values')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Trade-off visualization (Pareto front)
    ax = axes[1, 1]
    for alpha in alphas:
        fastest = experiments[alpha]['solutions']['fastest']
        cheapest = experiments[alpha]['solutions']['cheapest']
        balanced = experiments[alpha]['solutions']['balanced']
        
        ax.scatter(fastest['time'], fastest['cost'], color='blue', s=100, 
                   marker='o', label=f'α={alpha} (Fastest)' if alpha == alphas[0] else '')
        ax.scatter(cheapest['time'], cheapest['cost'], color='green', s=100, 
                   marker='s', label=f'α={alpha} (Cheapest)' if alpha == alphas[0] else '')
        ax.scatter(balanced['time'], balanced['cost'], color='red', s=100, 
                   marker='^', label=f'α={alpha} (Balanced)' if alpha == alphas[0] else '')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Cost')
    ax.set_title('Pareto Front: Trade-off Visualization')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cross_experiment_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: cross_experiment_analysis.png")
    plt.show()