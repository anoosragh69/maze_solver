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

def crossover(parents):
    import random
    children = []

    for _ in range(20):  # new population size
        p1 = random.choice(parents)
        p2 = random.choice(parents)

        cut = random.randint(1, min(len(p1), len(p2)) - 1)
        child = p1[:cut] + p2[cut:]

        children.append(child)

    return children

def mutate(population, rate=0.2):
    import random
    moves = ['N','S','E','W']

    for chrom in population:
        if random.random() < rate:
            idx = random.randint(0, len(chrom)-1)
            chrom[idx] = random.choice(moves)

    return population

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

population = [generate_valid_moves(m, steps=40) for _ in range(20)]

for gen in range(30):
    scores = [(moves, fitness(moves, m)) for moves in population]
    scores.sort(key=lambda x: x[1])

    print(f"Gen {gen} Best:", scores[0][1])

    # selection
    top = [moves for moves, _ in scores[:5]]

    # crossover
    children = crossover(top)

    # mutation
    population = mutate(children)

scores = [(moves, fitness(moves, m)) for moves in population]
scores.sort(key=lambda x: x[1])

best_moves = scores[0][0]

# --- agent ---
a = agent(m, footprints=True)

# --- build path ---
path = to_path(best_moves, m)

print("Path:", path)

# --- test ---
m.tracePath({a: path})
m.run()