import pygame
import random
import math
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
        self.outline = []
        self.shape_point_count = int(random.uniform(7, 15))
        for i in range(self.shape_point_count):
            angle = i * (360 / self.shape_point_count)
            distance = random.uniform(self.radius * 0.55, self.radius)
            self.outline.append((angle, distance))

    
    def draw(self, screen):
        # use the angle and distance from sel.outline to create the points of the polygon
        points = []
        for angle, distance in self.outline:
            angle_rad = math.radians(angle + self.rotation)
            x = self.position.x + math.cos(angle_rad) * distance
            y = self.position.y + math.sin(angle_rad) * distance
            points.append((x, y))

        pygame.draw.polygon(screen, (80, 80, 80), points)
        
    def update(self, dt):
        self.position += self.velocity * dt

        # Add screen wrapping logic
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
            
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius

    def split(self, player):

        # Point system based on the size of the asteroid
        if self.radius == ASTEROID_MAX_RADIUS:
            player.add_score(1)
        elif self.radius < ASTEROID_MAX_RADIUS and self.radius > ASTEROID_MIN_RADIUS:
            player.add_score(2)
        else:
            player.add_score(3)

        
        
        self.kill()

        random_angle = random.uniform(-40, 40)      
        vector_1 = self.velocity.rotate(random_angle)
        vector_2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        if self.radius <= ASTEROID_MIN_RADIUS:
            explosion = Explosion(self.position.x, self.position.y)
            return "this was a small asteroid"            
        else:
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_1.velocity = vector_1 * 1.3
            new_asteroid_2.velocity = vector_2 * 1.4
            explosion = Explosion(self.position.x, self.position.y)
        
        # Create an explosion effect
        
        

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(self.__class__.containers)
        self.position = pygame.math.Vector2(x, y)
        self.particle_count = EXPLOSION_PARTICLE_COUNT
        self.particles = []
        self.duration = EXPLOSION_DURATION
        self.age = 0

        # Initialize particles 
        for _ in range(self.particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(0.5, 6)
            direction = pygame.math.Vector2(
                math.cos(math.radians(angle)),
                math.sin(math.radians(angle))
            ) * speed
            self.particles.append({"position": self.position.copy(), "velocity": direction})

    def update(self, dt):
        self.age += 1
        if self.age > self.duration:
            self.particles = []  # Clear particles when expired
            return

        for particle in self.particles:
            particle["position"] += particle["velocity"]
            particle["velocity"] *= 0.9  # Slow down gradually

    def draw(self, screen):
        for particle in self.particles:
            position = particle["position"]  # Fetch the current particle position
            pygame.draw.circle(screen, (255, 180, 50), (int(position.x), int(position.y)), 2)