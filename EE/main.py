# main.py
import pygame
from game_settings import screen


from game_loop import game_loop

def main():
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()

    pygame.quit()

if __name__ == "__main__":
    main()
