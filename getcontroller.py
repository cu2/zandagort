"""
Handles all GET requests
"""

from controller import Controller


class GetController(Controller):
    """
    Handles all GET requests
    
    For details: see controller.py
    """
    
    def get_time(self):  # TEST
        """Return world time. Possibly just test method."""
        return self._game.get_time()
