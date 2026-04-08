from pyamaze import maze, agent
from utils import to_path
from ga import run_ga

# --- create maze ---
m = maze(5, 5)
m.CreateMaze()

best_moves = run_ga(m)

# --- agent ---
a = agent(m, footprints=True)

# --- build path ---
path = to_path(best_moves, m)

print("Path:", path)

# --- test ---
m.tracePath({a: path})
m.run()