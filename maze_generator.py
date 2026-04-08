from pyamaze import maze, agent

# --- create maze ---
m = maze(5, 5)
m.CreateMaze()

# --- movement function ---
def move(pos, d):
    if d == 'E': return (pos[0], pos[1] + 1)
    if d == 'W': return (pos[0], pos[1] - 1)
    if d == 'N': return (pos[0] - 1, pos[1])
    if d == 'S': return (pos[0] + 1, pos[1])

def fitness(moves, m):
    pos = (m.rows, m.cols)
    goal = (1,1)

    for d in moves:
        if m.maze_map[pos][d] == 1:
            pos = move(pos, d)

    # Manhattan distance to goal
    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])

# --- convert moves to path ---
def to_path(ch, m):
    pos = (m.rows, m.cols)
    path = {}

    for d in ch:
        if m.maze_map[pos][d] == 1:
            nxt = move(pos, d)
            path[pos] = nxt
            pos = nxt

    return path

# --- generate VALID moves ---
import random

def generate_valid_moves(m, steps=20):
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

# --- generate population ---
population = [generate_valid_moves(m, steps=40) for _ in range(20)]

# --- evaluate ---
scores = [(moves, fitness(moves, m)) for moves in population]
scores.sort(key=lambda x: x[1])  # lower is better

# --- best solution ---
best_moves = scores[0][0]

print("Best fitness:", scores[0][1])
print("Best moves:", best_moves)

# --- agent ---
a = agent(m, footprints=True)

# --- build path ---
path = to_path(best_moves, m)

print("Path:", path)

# --- test ---
m.tracePath({a: path})
m.run()