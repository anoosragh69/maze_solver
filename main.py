import random
from pyamaze import maze, agent
from utils import to_path
from ga import run_ga, evaluate_population, extract_solutions


def build_penalty_zones(m, time_zone_count=5, cost_zone_count=5):
    start = (m.rows, m.cols)
    goal = (1, 1)
    cells = [cell for cell in m.grid if cell not in (start, goal)]
    random.shuffle(cells)

    time_cells_end = min(time_zone_count, len(cells))
    cost_cells_end = min(time_cells_end + cost_zone_count, len(cells))
    time_cells = cells[:time_cells_end]
    cost_cells = cells[time_cells_end:cost_cells_end]

    time_penalties = {cell: random.randint(1, 4) for cell in time_cells}
    cost_penalties = {cell: random.randint(1, 4) for cell in cost_cells}
    return time_penalties, cost_penalties

# --- create maze ---
m = maze(5, 5)
m.CreateMaze()

final_population = run_ga(m, generations=40, population_size=40, chromosome_steps=45)
time_penalties, cost_penalties = build_penalty_zones(m)
evaluations = evaluate_population(final_population, m, time_penalties, cost_penalties)
solutions = extract_solutions(evaluations)

fastest_path = to_path(solutions["fastest"]["moves"], m)
cheapest_path = to_path(solutions["cheapest"]["moves"], m)
balanced_path = to_path(solutions["balanced"]["moves"], m)

print("\nExtracted solutions from a SINGLE evolution")
print(f"Final population size: {len(final_population)}")
print(
    f"Fastest Path   -> Time: {solutions['fastest']['total_time']}, Cost: {solutions['fastest']['total_cost']}"
)
print(
    f"Cheapest Path  -> Time: {solutions['cheapest']['total_time']}, Cost: {solutions['cheapest']['total_cost']}"
)
print(
    f"Balanced Path  -> Time: {solutions['balanced']['total_time']}, Cost: {solutions['balanced']['total_cost']}"
)

fastest_agent = agent(m, footprints=True, color="red")
cheapest_agent = agent(m, footprints=True, color="green")
balanced_agent = agent(m, footprints=True, color="blue")

m.tracePath(
    {
        fastest_agent: fastest_path,
        cheapest_agent: cheapest_path,
        balanced_agent: balanced_path,
    }
)
m.run()
