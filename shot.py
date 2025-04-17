import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    """
    Shot class that inherits from CircleShape.
    """
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        # Draw the shot as a circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
