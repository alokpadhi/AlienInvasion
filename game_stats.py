class GameStats():
    """Track statistics of the game"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start the game as active mode
        self.game_active = False
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
