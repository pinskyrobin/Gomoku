import pygame
from Macro import WINDOW

"""
def draw_chess(screen):
    player_one = (255, 251, 240)
    player_two = (88, 87, 86)
    player_color = [player_one, player_two]

    font = pygame.font.SysFont(None, WINDOW.REC_SIZE * 2 // 3)
    for i in range(len(self.steps)):
        x, y = self.steps[i]
        map_x, map_y, width, height = self.getMapUnitRect(x, y)
        pos, radius = (map_x + width // 2, map_y + height // 2), WINDOW.CHESS_RADIUS
        turn = self.map[y][x]
        if turn == 1:
            op_turn = 2
        else:
            op_turn = 1
        pygame.draw.circle(screen, player_color[turn - 1], pos, radius)

        msg_image = font.render(str(i), True, player_color[op_turn - 1], player_color[turn - 1])
        msg_image_rect = msg_image.get_rect()
        msg_image_rect.center = pos
        screen.blit(msg_image, msg_image_rect)

    if len(self.steps) > 0:
        last_pos = self.steps[-1]
        map_x, map_y, width, height = self.getMapUnitRect(last_pos[0], last_pos[1])
        purple_color = (255, 0, 255)
        point_list = [(map_x, map_y), (map_x + width, map_y),
                      (map_x + width, map_y + height), (map_x, map_y + height)]
        pygame.draw.lines(screen, purple_color, True, point_list, 1)

"""


def draw_background(screen):
    color = (0, 0, 0)
    for y in range(WINDOW.MAP_HEIGHT):
        # draw a horizontal line
        start_pos, end_pos = (WINDOW.REC_SIZE // 2, WINDOW.REC_SIZE // 2 + WINDOW.REC_SIZE * y), (
            WINDOW.MAP_WIDTH - WINDOW.REC_SIZE // 2, WINDOW.REC_SIZE // 2 + WINDOW.REC_SIZE * y)
        width = 2
        pygame.draw.line(screen, color, start_pos, end_pos, width)

    for x in range(WINDOW.MAP_WIDTH):
        # draw a horizontal line
        start_pos, end_pos = (WINDOW.REC_SIZE // 2 + WINDOW.REC_SIZE * x, WINDOW.REC_SIZE // 2), (
            WINDOW.REC_SIZE // 2 + WINDOW.REC_SIZE * x, WINDOW.MAP_HEIGHT - WINDOW.REC_SIZE // 2)
        width = 2
        pygame.draw.line(screen, color, start_pos, end_pos, width)

    rec_size = 8
    pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
    for (x, y) in pos:
        pygame.draw.rect(screen, color, (
            WINDOW.REC_SIZE // 2 + x * WINDOW.REC_SIZE - WINDOW.REC_SIZE // 2,
            WINDOW.REC_SIZE // 2 + y * WINDOW.REC_SIZE - rec_size // 2, rec_size,
            rec_size))


class game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW.SCREEN_WIDTH, WINDOW.SCREEN_HEIGHT])
        light_yellow = (247, 238, 214)
        pygame.draw.rect(self.screen, light_yellow, pygame.Rect(0, 0, WINDOW.MAP_WIDTH, WINDOW.SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(WINDOW.MAP_WIDTH, 0, WINDOW.INFO_WIDTH, WINDOW.SCREEN_HEIGHT))
        draw_background(self.screen)
