import pygame
import math
from pathlib import Path
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
        self.rotation = 180
        self.timer = 0
        self.score = 0
        self.lives = PLAYER_LIVES
        self.invulnerable = False
        self.invulnerable_duration = PLAYER_INVULNERABLE_DURATION
        self.invulnerable_time = 0
        self.velocity = pygame.Vector2(0, 0)
        self.is_accelerating = False

        self.ship_only = pygame.image.load(Path("assets/rocket.png")).convert_alpha()
        self.ship_with_flame = pygame.image.load(Path("assets/rocket - fire.png")).convert_alpha()

        self.thruster_sound = pygame.mixer.Sound("assets/Thrust.wav")
        self.thruster_sound.set_volume(THRUSTER_VOLUME)
        self.laser_sound = pygame.mixer.Sound("assets/Laser_shoot2.wav")
        self.laser_sound.set_volume(LAZER_VOLUME)

        original_width = self.ship_only.get_width()
        original_height = self.ship_only.get_height()
        
        aspect_ratio = original_width / original_height        
        new_height = PLAYER_RADIUS * 5
        new_width = int(new_height * aspect_ratio)
        
        self.ship_only = pygame.transform.scale(self.ship_only, (new_width, new_height))
        self.ship_with_flame = pygame.transform.scale(self.ship_with_flame, (new_width, new_height))
        
        self.ship_only = pygame.transform.rotate(self.ship_only, 180)
        self.ship_with_flame = pygame.transform.rotate(self.ship_with_flame, 180)
        
        self.image = self.ship_only


        


    # triangle method to get the vertices of the triangle representing the player
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.is_accelerating:
            current_image = self.ship_with_flame
            self.thruster_sound.play()
        if not self.is_accelerating:
            self.thruster_sound.stop()  
            current_image = self.ship_only
        
        rotated_image = pygame.transform.rotate(current_image, -self.rotation)
        
        triangle_points = self.triangle()
        triangle_center = pygame.Vector2(
            (triangle_points[0].x + triangle_points[1].x + triangle_points[2].x) / 3,
            (triangle_points[0].y + triangle_points[1].y + triangle_points[2].y) / 3
        )

        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Apply offset to match hit box with the image
        offset_amount = -18  
        offset_position = triangle_center + forward_vector * offset_amount
        image_rect = rotated_image.get_rect(center=offset_position)

        if not self.invulnerable or int(self.invulnerable_time * 5) % 2 == 0:
            screen.blit(rotated_image, image_rect)
        # Uncomment for debugging hitbox
        # pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)    
    
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
        if self.invulnerable:
            self.invulnerable_time += dt
            if self.invulnerable_time >= self.invulnerable_duration:
                self.invulnerable = False
                self.invulnerable_time = 0
        
        self.is_accelerating = False
        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.is_accelerating = True
            self.move(dt, 1)
            self.thruster_sound.play()  # Play the sound continuously while accelerating
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
        self.laser_sound.play()

        # shooting from the tip of the triangle
        bullet = Shot(self.triangle()[0][0], self.triangle()[0][1])
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def add_score(self, score):
        self.score += score
    
    def collide(self, other):
        # Check if the player is invulnerable
        if self.invulnerable:
            return False

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
                    if self.lives > 1:
                        explosion = Explosion(self.position.x, self.position.y)
                    return True       
        return False
    
    def reset(self):
        self.invulnerable = True
        self.invulnerable_time = 0
        self.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 180
        self.lives -= 1



        