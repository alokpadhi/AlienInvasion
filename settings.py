class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Ship setting
        # self.ship_speed_factor = 1.4
        self.ship_limit = 3
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (190, 190, 190)
        # Bullet Settings
        # self.bullet_speed_factor = 2
        self.bullet_width = 8
        self.bullet_height = 26
        self.bullet_color = 0, 0, 0
        self.bullets_allowed = 3
        # Alien / Zombie settings
        # self.alien_speed_factor = 0.3
        self.fleet_drop_speed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        self.ship_speed_factor = 1.4
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.4

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increase the speed settings and alien point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
