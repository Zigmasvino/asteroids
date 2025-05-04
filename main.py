import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from game_over_screen import Draw_game_over_screen



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
    pygame.mixer.init()

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
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Load the background image
    background = pygame.image.load('backround_image.jpg').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))    

     # Add the player to the updatable and drawable groups
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)  
    field = AsteroidField()

    game_state = "playing"
    play_again_rect = None
    exit_button_rect = None

    # Infinite loop to keep the game running
    while True:
        # to be able to close the game        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                return
                
            if game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:        
                if exit_button_rect and exit_button_rect.collidepoint(event.pos):
                    print("Exit clicked!")
                    return                
                if play_again_rect and play_again_rect.collidepoint(event.pos):
                    print("Play Again clicked!")
                    player.lives = PLAYER_LIVES                    
                    game_state = "playing"                    
        
        # Set the background
        screen.blit(background, (0, 0))

        draw_score(screen, player.score, player.lives)  
        
        if game_state == "playing":            
            updatable.update(dt)

            # Checking for Player and asteroid collision
            for asteroid in asteroids:
                if player.collide(asteroid) and player.lives > 1:
                    player.reset()
                    print(f"Player lives: {player.lives}")
                    asteroid.kill()
                if player.collide(asteroid) and player.lives <= 1:
                    print("GAME OVER!")
                    player.reset()
                    game_state = "game_over"
            
            # Checking for bullet and asteroid collisiond
            for asteroid in asteroids:
                for bullet in shots:
                    if bullet.collide(asteroid):
                        bullet.kill()
                        asteroid.split(player)

            for sprite in drawable:            
                sprite.draw(screen)

        elif game_state == "game_over":
            for asteroid in asteroids:
                asteroid.kill()
            play_again_rect, exit_button_rect = Draw_game_over_screen(screen)  
        
        pygame.display.flip()
        dt = clock.tick(120) / 1000.0    

    
if __name__ == "__main__":
    main()