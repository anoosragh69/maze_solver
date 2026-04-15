import numpy as np

class CostMaze:
    """Maze with time and cost penalties for regions"""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze_structure = {}  # Wall/passage info from pyamaze
        
        # Initialize cost maps
        self.time_cost = np.ones((rows + 2, cols + 2))  # Default time = 1
        self.money_cost = np.ones((rows + 2, cols + 2))  # Default cost = 1
        
    def define_regions(self):
        """Define different regions with different costs"""
        # Region 1: Swamp (slow but cheap) - rows 2-3, cols 2-3
        self.time_cost[2:4, 2:4] = 5.0    # Takes 5x longer
        self.money_cost[2:4, 2:4] = 0.5   # Costs half price
        
        # Region 2: Highway (fast but expensive) - rows 3-4, cols 4-5
        self.time_cost[3:5, 4:6] = 0.5    # Takes half the time
        self.money_cost[3:5, 4:6] = 3.0   # Costs 3x more
        
        # Region 3: Mountain (expensive but faster shortcuts)
        self.time_cost[1:3, 4:6] = 2.0
        self.money_cost[1:3, 4:6] = 2.5
        
    def get_cell_cost(self, pos):
        """Returns (time_cost, money_cost) for a cell"""
        if 0 <= pos[0] < self.rows + 2 and 0 <= pos[1] < self.cols + 2:
            return self.time_cost[pos], self.money_cost[pos]
        return 1.0, 1.0