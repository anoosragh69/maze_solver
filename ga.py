import random
from utils import move

def generate_valid_moves(m, steps=100):
    pos = (m.rows, m.cols)
    moves = []

    for _ in range(steps):
        valid_dirs = [d for d in 'ESNW' if m.maze_map[pos][d] == 1]
        if not valid_dirs:
            break
        d = random.choice(valid_dirs)
        moves.append(d)
        pos = move(pos, d)
        if pos == (1, 1):
            break

    return moves

def run_path(moves, m):
    pos = (m.rows, m.cols)
    goal = (1,1)
    
    path_len = 0
    for d in moves:
        if m.maze_map[pos][d] == 1:
            pos = move(pos, d)
            path_len += 1
            if pos == goal:
                break
    return pos, path_len

def fitness(moves, m):
    pos, path_len = run_path(moves, m)
    goal = (1,1)

    dist = abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
    
    score = dist * 1000 + path_len
    return score

def crossover(parents, pop_size):
    import random
    children = []

    for _ in range(pop_size - len(parents)):
        p1 = random.choice(parents)
        p2 = random.choice(parents)

        if len(p1) > 1 and len(p2) > 1:
            cut1 = random.randint(1, len(p1) - 1)
            cut2 = random.randint(1, len(p2) - 1)
            child = p1[:cut1] + p2[cut2:]
        else:
            child = p1[:]
        children.append(child)

    return parents + children

def mutate(population, rate=0.2):
    import random
    moves = ['N','S','E','W']

    for i in range(len(population)):
        if random.random() < rate:
            chrom = population[i]
            if len(chrom) > 0:
                idx = random.randint(0, len(chrom)-1)
                chrom[idx] = random.choice(moves)
                if random.random() < 0.5:
                    chrom.insert(idx, random.choice(moves))
                elif len(chrom) > 1:
                    chrom.pop(idx)
            population[i] = chrom

    return population

def run_ga(m, generations=100, population_size=100):
    max_steps = m.rows * m.cols * 2
    population = [generate_valid_moves(m, steps=max_steps) for _ in range(population_size)]

    for gen in range(generations):
        scores = [(moves, fitness(moves, m)) for moves in population]
        scores.sort(key=lambda x: x[1])

        best_fitness = scores[0][1]
        if gen % 20 == 0:
            print(f"Gen {gen} Best Fitness: {best_fitness}")

        top_count = max(2, population_size // 5)
        top = [moves for moves, _ in scores[:top_count]]

        population = crossover(top, population_size)

        best_org = population[0]
        rest = mutate(population[1:], rate=0.3)
        population = [best_org] + rest

    return population