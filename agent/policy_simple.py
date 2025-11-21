import random
from typing import Dict, Any

class SimplePolicyAgent:
    """
    A heuristic-based agent.
    """
    
    def __init__(self):
        pass
        
    def decide_action(self, state: Dict[str, Any]) -> str:
        """
        Decide the next move based on the current state.
        
        Args:
            state: The structured game state from StateEstimator.
            
        Returns:
            One of 'UP', 'DOWN', 'LEFT', 'RIGHT'.
        """
        # TODO: 
        # 1. Check for immediate ghost danger.
        # 2. If safe, find path to nearest pellet.
        # 3. Return first step of that path.
        
        # MVP: Random walk
        return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
