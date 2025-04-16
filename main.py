import pygame
from constants import *
from player import Player

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
    
    Player.containers = updatable, drawable

    # Add the player to the updatable and drawable groups
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Infinite loop to keep the game running
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                return
        
        # Fill the screen with black 
        screen.fill((0, 0, 0))
        
        # Update the game objects
        updatable.update(dt)

        for sprite in drawable:            
            # Draw the game objects
            sprite.draw(screen)      
                   
        
        pygame.display.flip()
        # dt is the time since the last frame in seconds
        dt = clock.tick(60) / 1000.0
        # Limit the frame rate to 60 FPS
        clock.tick(60)

    

    
if __name__ == "__main__":
    main()