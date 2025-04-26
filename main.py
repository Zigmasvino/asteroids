import pygame
import sys
import os
from constants import *
from player import Player
from asteroid import Asteroid, Explosion
from asteroidfield import AsteroidField
from shot import Shot


def draw_score(screen, score, lives):
    """
    Draw the score on the screen.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


def main():
    # Initialize the game
    pygame.init()
    print("Starting Asteroids!")
    pygame.font.init()

    # Set up the game clock
    clock = pygame.time.Clock()
    # Time since the last frame in seconds
    dt = 0

    # Setting up sprite groups - these are used to manage and update the game objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = updatable, drawable
    Asteroid.containers = updatable, drawable, asteroids
    AsteroidField.containers = updatable
    Shot.containers = shots, drawable, updatable
    Explosion.containers = drawable,updatable

    # Add the player to the updatable and drawable groups
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)  
    field = AsteroidField()
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Load the background image
    background = pygame.image.load('backround_image.jpg').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Infinite loop to keep the game running
    while True:
        # to be able to close the game        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                return
        
        # Fill the screen with black 
        # screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        # Update the game objects
        updatable.update(dt)

        # Checking for Player and asteroid collision
        for asteroid in asteroids:            
            if asteroid.collide(player) and player.lives <= 1:
                print("GAME OVER!")
                sys.exit()
            else:
                if asteroid.collide(player):
                    player.lives -= 1
                    player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    player.velocity = pygame.Vector2(0, 0)
                    player.rotation = 0
                    print(f"Player lives: {player.lives}")
                    asteroid.kill()
        
        # Checking for bullet and asteroid collisiond
        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collide(asteroid):
                    bullet.kill()
                    asteroid.split(player)

        # Draw the game objects
        for sprite in drawable:            
            sprite.draw(screen)

        # Draw the score
        draw_score(screen, player.score, player.lives)     
                   
        
        pygame.display.flip()
        # dt is the time since the last frame in seconds
        dt = clock.tick(60) / 1000.0
        # Limit the frame rate to 60 FPS
        clock.tick(60)

    

    
if __name__ == "__main__":
    main()