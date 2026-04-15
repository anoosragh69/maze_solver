import numpy as np

class CostMaze:
    """Maze with time and cost penalties for regions"""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze_structure = {}  # Wall/passage info from pyamaze
        self.maze_map = {}       # Will be set from pyamaze
        
        # Initialize cost maps (extra padding for safety)
        self.time_cost = np.ones((rows + 2, cols + 2))  # Default time = 1
        self.money_cost = np.ones((rows + 2, cols + 2))  # Default cost = 1
        
    def define_regions(self):
        """Define different regions with different costs.
        Regions scale with maze size for visual variety.
        """
        r, c = self.rows, self.cols

        # Region 1: Swamp (slow but cheap) — middle-left area
        r1_start, r1_end = max(1, r // 3), min(r + 1, 2 * r // 3 + 1)
        c1_start, c1_end = max(1, c // 4), min(c + 1, c // 2 + 1)
        self.time_cost[r1_start:r1_end, c1_start:c1_end] = 5.0    # Takes 5× longer
        self.money_cost[r1_start:r1_end, c1_start:c1_end] = 0.5   # Costs half price
        
        # Region 2: Highway (fast but expensive) — lower-right area
        r2_start, r2_end = max(1, r // 2 + 1), min(r + 1, 3 * r // 4 + 1)
        c2_start, c2_end = max(1, c // 2 + 1), min(c + 1, c + 1)
        self.time_cost[r2_start:r2_end, c2_start:c2_end] = 0.5    # Takes half the time
        self.money_cost[r2_start:r2_end, c2_start:c2_end] = 3.0   # Costs 3× more
        
        # Region 3: Mountain (expensive and somewhat slow)
        r3_start, r3_end = max(1, 1), min(r + 1, r // 3 + 1)
        c3_start, c3_end = max(1, c // 2 + 1), min(c + 1, c + 1)
        self.time_cost[r3_start:r3_end, c3_start:c3_end] = 2.0
        self.money_cost[r3_start:r3_end, c3_start:c3_end] = 2.5
        
    def get_cell_cost(self, pos):
        """Returns (time_cost, money_cost) for a cell"""
        if 0 <= pos[0] < self.time_cost.shape[0] and 0 <= pos[1] < self.time_cost.shape[1]:
            return self.time_cost[pos], self.money_cost[pos]
        return 1.0, 1.0