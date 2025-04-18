import pygame
import random
from constants import *
from circleshape import CircleShape
from player import Player

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

    def split(self, player):
        player.add_score(1)
        self.kill()
        random_angle = random.uniform(-30, 30)      
        vector_1 = self.velocity.rotate(random_angle)
        vector_2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        if self.radius <= ASTEROID_MIN_RADIUS:
            return "this was a small asteroid"
        else:
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_1.velocity = vector_1 * 1.3
            new_asteroid_2.velocity = vector_2 * 1.4