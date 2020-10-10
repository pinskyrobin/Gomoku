import pygame

from Macro import PLAY_MODE, OPPONENT_LEVEL, PLAY_STATUS
from Play import play
from Game import game
from PlayTheGame import play_game

"""
while True:
    game()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
"""


play_game(PLAY_STATUS.NOT_SURE, PLAY_MODE.MACHINE_MACHINE)
