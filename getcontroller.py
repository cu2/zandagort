from controller import Controller


class GetController(Controller):
    """Handles all GET requests"""
    
    def get_time(self):
        return self._game.get_time()
