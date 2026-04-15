import random

def move(pos, d):
    if d == 'E': return (pos[0], pos[1] + 1)
    if d == 'W': return (pos[0], pos[1] - 1)
    if d == 'N': return (pos[0] - 1, pos[1])
    if d == 'S': return (pos[0] + 1, pos[1])

def to_path(ch, m):
    pos = (m.rows, m.cols)
    path = {}
    path_list = [pos]

    for d in ch:
        if m.maze_map[pos][d] == 1:
            nxt = move(pos, d)
            path[pos] = nxt
            pos = nxt
            path_list.append(pos)
            if pos == (1, 1):
                break

    return path, path_list

def generate_penalty_zones(rows, cols, time_prob=0.3, cost_prob=0.3):
    time_zones = {}
    cost_zones = {}
    
    # Base: normal cells have time 1, cost 1
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            time_zones[(r, c)] = 1
            cost_zones[(r, c)] = 1

    # Q2 (Top-Right): Cost Trap (huge cost, low time)
    for r in range(1, rows//2 + 1):
        for c in range(cols//2 + 1, cols + 1):
            cost_zones[(r, c)] = 50
            time_zones[(r, c)] = 1
            
    # Q3 (Bottom-Left): Time Trap (huge time, low cost)
    for r in range(rows//2 + 1, rows + 1):
        for c in range(1, cols//2 + 1):
            cost_zones[(r, c)] = 1
            time_zones[(r, c)] = 50

    # Center Square: Balanced Trap (medium cost, medium time)
    # This allows a diagonal path to be distinctly balanced
    for r in range(rows//2 - 1, rows//2 + 2):
        for c in range(cols//2 - 1, cols//2 + 2):
            if 1 <= r <= rows and 1 <= c <= cols:
                cost_zones[(r, c)] = 15
                time_zones[(r, c)] = 15

    # Guarantee start and goal don't have crazy penalties
    time_zones[(rows, cols)] = 1
    cost_zones[(rows, cols)] = 1
    time_zones[(1, 1)] = 1
    cost_zones[(1, 1)] = 1
    
    return time_zones, cost_zones

def evaluate_path(path_list, time_zones, cost_zones):
    total_time = 0
    total_cost = 0
    for cell in path_list:
        total_time += time_zones.get(cell, 1)
        total_cost += cost_zones.get(cell, 0)
    return total_time, total_cost