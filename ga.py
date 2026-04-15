import random
from utils import move

GOAL_REACHED_FITNESS_ADJUSTMENT = -5
ELITE_RATIO = 0.2
INVALID_PATH_PENALTY = 1000

def trace_moves(moves, m):
    pos = (m.rows, m.cols)
    goal = (1, 1)
    cells = [pos]

    for d in moves:
        if m.maze_map[pos][d] == 1:
            pos = move(pos, d)
            cells.append(pos)
        if pos == goal:
            break

    return cells, pos, pos == goal


def generate_valid_moves(m, steps=20):
    pos = (m.rows, m.cols)
    goal = (1, 1)
    moves = []

    for _ in range(steps):
        valid_dirs = [d for d in "ESNW" if m.maze_map[pos][d] == 1]
        if not valid_dirs:
            break
        d = random.choice(valid_dirs)
        moves.append(d)
        pos = move(pos, d)
        if pos == goal:
            break

    return moves


def repair_moves(moves, m, max_steps=40):
    pos = (m.rows, m.cols)
    goal = (1, 1)
    repaired = []

    for d in moves[:max_steps]:
        valid_dirs = [d for d in "ESNW" if m.maze_map[pos][d] == 1]
        if not valid_dirs:
            break
        chosen = d if d in valid_dirs else random.choice(valid_dirs)
        repaired.append(chosen)
        pos = move(pos, chosen)
        if pos == goal:
            break

    return repaired


def fitness(moves, m):
    cells, end_pos, reached_goal = trace_moves(moves, m)
    goal = (1, 1)
    distance = abs(end_pos[0] - goal[0]) + abs(end_pos[1] - goal[1])
    revisit_penalty = len(cells) - len(set(cells))
    goal_bonus = GOAL_REACHED_FITNESS_ADJUSTMENT if reached_goal else 0
    return distance + 0.2 * revisit_penalty + goal_bonus


def crossover(parents, population_size=20):
    children = []
    if not parents:
        return children

    for _ in range(population_size):
        p1 = random.choice(parents)
        p2 = random.choice(parents)
        min_len = min(len(p1), len(p2))

        if min_len < 2:
            child = list(p1 if len(p1) >= len(p2) else p2)
        else:
            cut = random.randint(1, min_len - 1)
            child = p1[:cut] + p2[cut:]
        children.append(child)

    return children


def mutate(population, m, rate=0.2):
    for i, chrom in enumerate(population):
        if chrom and random.random() < rate:
            idx = random.randint(0, len(chrom) - 1)
            chrom[idx] = random.choice(["N", "S", "E", "W"])
            population[i] = repair_moves(chrom, m)
    return population


def run_ga(m, generations=30, population_size=20, max_path_length=40):
    population_size = max(3, population_size)
    population = [generate_valid_moves(m, steps=max_path_length) for _ in range(population_size)]

    for gen in range(generations):
        population = [repair_moves(chrom, m, max_steps=max_path_length) for chrom in population]
        scores = [(moves, fitness(moves, m)) for moves in population]
        scores.sort(key=lambda x: x[1])
        print(f"Gen {gen} Best:", scores[0][1])

        desired_elites = max(1, int(population_size * ELITE_RATIO))
        max_elites = max(1, population_size - 2)
        elite_count = min(desired_elites, max_elites)
        elites = [list(moves) for moves, _ in scores[:elite_count]]
        # Keep one slot for an immigrant to preserve exploration diversity.
        children_count = max(0, population_size - elite_count - 1)
        children = crossover(elites, population_size=children_count)
        children = mutate(children, m)
        immigrant = generate_valid_moves(m, steps=max_path_length)

        population = elites + children + [immigrant]

    return [repair_moves(chrom, m, max_steps=max_path_length) for chrom in population]


def evaluate_population(population, m, time_penalties, cost_penalties, invalid_penalty=INVALID_PATH_PENALTY):
    evaluations = []

    for moves in population:
        cells, _, reached_goal = trace_moves(moves, m)
        steps = max(0, len(cells) - 1)
        # Exclude the start cell from penalties; only traversed maze regions add penalties.
        # Non-goal-reaching paths are still discouraged by invalid_penalty below.
        time_penalty = sum(time_penalties.get(cell, 0) for cell in cells[1:])
        cost_penalty = sum(cost_penalties.get(cell, 0) for cell in cells[1:])
        total_time = steps + time_penalty
        total_cost = steps + cost_penalty

        if not reached_goal:
            total_time += invalid_penalty
            total_cost += invalid_penalty

        evaluations.append(
            {
                "moves": moves,
                "total_time": total_time,
                "total_cost": total_cost,
                "balanced_score": total_time + total_cost,
                "reached_goal": reached_goal,
            }
        )

    return evaluations


def extract_solutions(evaluations):
    valid_pool = [item for item in evaluations if item["reached_goal"]]
    if not valid_pool:
        valid_pool = evaluations
    return {
        "fastest": min(valid_pool, key=lambda item: item["total_time"]),
        "cheapest": min(valid_pool, key=lambda item: item["total_cost"]),
        "balanced": min(valid_pool, key=lambda item: item["balanced_score"]),
    }
