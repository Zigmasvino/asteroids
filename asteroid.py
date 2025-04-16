import pygame
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    """
    Asteroid class that inherits from CircleShape.
    """
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0        
        self.rotation_speed = 0
    
    def draw(self, screen):
        # Draw the asteroid as a circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt