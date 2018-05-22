import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single zombie in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien/zombie and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the zombie/alien image and set its rect attribute
        self.image = pygame.image.load('images/zombie.bmp')
        self.rect = self.image.get_rect()

        # Start each zombie near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the zombie's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the zombie at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien / zombie right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien/zombie hits edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
