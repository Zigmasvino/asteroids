import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    """
    Shot class that inherits from CircleShape.
    """
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.laser_length = 15

    def draw(self, screen):
        if self.velocity.length() > 0:
            # Normalize velocity and multiply by laser length
            direction = self.velocity.normalize() * self.laser_length
            start_pos = self.position - direction / 2
            end_pos = self.position + direction / 2
            
            # Draw the laser as a line
            laser_color = (57, 255, 20)  
            pygame.draw.line(screen, laser_color, 
                            (int(start_pos.x), int(start_pos.y)),
                            (int(end_pos.x), int(end_pos.y)), 3)  # Width of 3

        # # Draw the shot as a circle
        # pygame.draw.circle(screen, (224, 17, 95), (int(self.position.x), int(self.position.y)), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
