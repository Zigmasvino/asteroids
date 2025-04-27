import pygame
import math
from constants import *
from circleshape import CircleShape
from shot import Shot
from explosion import Explosion
from static import segments_intersect




class Player(CircleShape):
    """
    Player class that inherits from CircleShape.
    """
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.score = 0
        self.lives = PLAYER_LIVES
        self.velocity = pygame.Vector2(0, 0)

    # triangle method to get the vertices of the triangle representing the player
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # Draw the player as a triangle
        pygame.draw.polygon(screen, (135, 134, 129), self.triangle())
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
    
    def rotate(self, dt):
        # Rotate the player
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt, direction=1):
         # Instead of directly changing position, apply acceleration to velocity
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Accelerate in the direction we're facing
        self.velocity += forward * PLAYER_ACCELERATION * direction * dt
        # Optional: limit maximum velocity
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)
        if keys[pygame.K_SPACE] and self.timer < 0:
            self.shoot()

        # Apply friction to gradually slow down
        self.velocity *= (1 - PLAYER_FRICTION * dt)        
        # Update position based on velocity
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
    
    def shoot(self):
        self.timer = PLAYER_SHOOT_COOLDOWN
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def add_score(self, score):
        self.score += score
    
    def collide(self, other):
        triangle = self.triangle()
        asteroid_x_y = other.get_polygon_points()

        # Check if the triangle intersects with the polygon
        for i in range(3):
            T1 = triangle[i]
            T2 = triangle[(i + 1) % 3]
            # Check if the line segment T1-T2 intersects with the circle
            for j in range(len(asteroid_x_y)):
                A = asteroid_x_y[j]
                B = asteroid_x_y[(j + 1) % len(asteroid_x_y)]
                if segments_intersect(T1, T2, A, B):
                    explosion = Explosion(self.position.x, self.position.y)
                    return True       
        return False



        