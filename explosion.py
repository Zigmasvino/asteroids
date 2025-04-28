import pygame
import random
import math
from constants import *


class Explosion(pygame.sprite.Sprite):
    """
    Explosion class that creates a visual effect of an explosion.
    It generates particles that move outward from the explosion center.
    """
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
            speed = random.uniform(EXPLOSION_MIN_SPEED, EXPLOSION_MAX_SPEED)
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
            particle["velocity"] *= EXPLOSION_FRICTION  # Slow down gradually

    def draw(self, screen):
        for particle in self.particles:
            position = particle["position"]  # Fetch the current particle position
            pygame.draw.circle(screen, (255, 180, 50), (int(position.x), int(position.y)), 2)