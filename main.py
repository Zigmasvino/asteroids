import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # Initialize the game
    pygame.init()
    print("Starting Asteroids!")

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

    # Add the player to the updatable and drawable groups
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)  
    field = AsteroidField()
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Infinite loop to keep the game running
    while True:
        # to be able to close the game       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                return
        
        # Fill the screen with black 
        screen.fill((0, 0, 0))
        
        # Update the game objects
        updatable.update(dt)

        for asteroid in asteroids:            
            if asteroid.collide(player):
                print("GAME OVER!")
                sys.exit()

        # Draw the game objects
        for sprite in drawable:            
            sprite.draw(screen)      
                   
        
        pygame.display.flip()
        # dt is the time since the last frame in seconds
        dt = clock.tick(60) / 1000.0
        # Limit the frame rate to 60 FPS
        clock.tick(60)

    

    
if __name__ == "__main__":
    main()