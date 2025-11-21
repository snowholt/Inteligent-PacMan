from typing import List, Tuple

class PathFinder:
    """
    Handles pathfinding algorithms (BFS, A*) on the grid.
    """
    
    def __init__(self):
        pass
        
    def find_path(self, grid, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find a path from start to goal avoiding walls.
        
        Args:
            grid: The game grid.
            start: (x, y)
            goal: (x, y)
            
        Returns:
            List of (x, y) coordinates representing the path.
        """
        # TODO: Implement A* or BFS.
        return []

    def find_nearest_pellet(self, grid, start: Tuple[int, int]) -> Tuple[int, int]:
        """Find the coordinates of the nearest safe pellet."""
        # TODO: BFS search for nearest pellet.
        return None
