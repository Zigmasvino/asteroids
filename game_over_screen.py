import pygame
from constants import *


def Draw_game_over_screen(screen):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with alpha for transparency
    screen.blit(overlay, (0, 0))
    
    # Draw "GAME OVER" text
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    screen.blit(text, text_rect)
    
    # Draw buttons
    button_width, button_height = 200, 50
    button_y = SCREEN_HEIGHT * 2/3
    
    # PLAY AGAIN button
    play_again_rect = pygame.Rect(SCREEN_WIDTH/2 - button_width - 20, button_y, button_width, button_height)
    pygame.draw.rect(screen, (0, 200, 0), play_again_rect)
    
    button_font = pygame.font.Font(None, 36)
    play_text = button_font.render("PLAY AGAIN", True, (255, 255, 255))
    play_text_rect = play_text.get_rect(center=play_again_rect.center)
    screen.blit(play_text, play_text_rect)
    
    # EXIT button
    exit_rect = pygame.Rect(SCREEN_WIDTH/2 + 20, button_y, button_width, button_height)
    pygame.draw.rect(screen, (200, 0, 0), exit_rect)
        
    exit_text = button_font.render("EXIT", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_rect.center)
    screen.blit(exit_text, exit_text_rect)

    # Return the button rectangles so they can be used for collision detection
    return play_again_rect, exit_rect