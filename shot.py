import pygame
from constants import *
from circleshape import CircleShape
from static import segments_intersect

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
    
    def collide_with_asteroid(self, asteroid):
        # Calculate laser start and end points
        direction = self.velocity.normalize() * self.laser_length
        start_pos = self.position - direction / 2
        end_pos = self.position + direction / 2
        
        asteroid_points = asteroid.get_polygon_points()
        
        # Check if the laser line intersects with any asteroid edge
        for i in range(len(asteroid_points)):
            A = asteroid_points[i]
            B = asteroid_points[(i + 1) % len(asteroid_points)]
            
            if segments_intersect((start_pos.x, start_pos.y), 
                                    (end_pos.x, end_pos.y), A, B):
                return True
                
        return False