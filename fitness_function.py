from utils import move
def calculate_path_metrics(moves, maze_obj):
    """Calculate total time and cost for a path"""
    pos = (maze_obj.rows, maze_obj.cols)
    goal = (1, 1)
    
    total_time = 0.0
    total_cost = 0.0
    path_length = 0
    reached_goal = False
    
    for direction in moves:
        if maze_obj.maze_map[pos][direction] == 1:  # Valid move
            pos = move(pos, direction)
            path_length += 1
            
            # Get cell costs
            time_c, cost_c = maze_obj.get_cell_cost(pos)
            total_time += time_c
            total_cost += cost_c
            
            # Check if reached goal
            if pos == goal:
                reached_goal = True
                break
        else:
            # Penalize running into walls so it doesn't "cheat" by staying still
            total_time += 2.0
            total_cost += 2.0
    
    # Penalty for not reaching goal
    if not reached_goal:
        manhattan = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        # Massive penalty so reaching the goal is ALWAYS strictly better
        # than stopping short, even if the path there is very expensive.
        total_time += manhattan * 100.0  
        total_cost += manhattan * 100.0
        
    return total_time, total_cost, path_length

def combined_fitness(moves, maze_obj, alpha=0.5, normalize=True):
    """
    Combined fitness function
    
    Args:
        moves: sequence of direction moves
        maze_obj: CostMaze object
        alpha: weight for cost (0.0 = prioritize time, 1.0 = prioritize cost)
        normalize: whether to normalize metrics
    
    Returns:
        fitness_score (lower is better)
    """
    total_time, total_cost, path_length = calculate_path_metrics(moves, maze_obj)
    
    # Normalization (optional but recommended)
    if normalize:
        # Scale to reasonable ranges (e.g., 0-100)
        normalized_time = min(total_time / 50.0, 100)  # Normalize based on max expected
        normalized_cost = min(total_cost / 50.0, 100)
    else:
        normalized_time = total_time
        normalized_cost = total_cost
    
    # Weighted combination
    fitness_score = (1 - alpha) * normalized_time + alpha * normalized_cost
    
    return fitness_score, total_time, total_cost, path_length

def fitness_time_optimized(moves, maze_obj):
    """Extract time metric (for selecting fastest path)"""
    _, total_time, _ = calculate_path_metrics(moves, maze_obj)
    return total_time

def fitness_cost_optimized(moves, maze_obj):
    """Extract cost metric (for selecting cheapest path)"""
    _, _, total_cost = calculate_path_metrics(moves, maze_obj)
    return total_cost