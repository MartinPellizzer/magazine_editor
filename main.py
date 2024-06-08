import pygame
from pygame.locals import *
from sys import exit

background_image = 'assets/bg-image.jpg'
mouse_image = 'assets/bg-image.jpg'

pygame.init()

a4_w = 2480
a4_h = 3508

page_w = 248*2
page_h = 351*2

window_w = 1280
window_h = 720



screen = pygame.display.set_mode((window_w, window_h), 0, 32)

pygame.display.set_caption("Magazine Editor")

background = pygame.image.load(background_image).convert()
mouse_cursor = pygame.image.load(mouse_image).convert()

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
    
    # screen.blit(background, (0, 0))
    
    # x, y = pygame.mouse.get_pos()
    # screen.blit(mouse_cursor, (x, y))

    # draw page
    page_x = window_w//2-page_w//2
    page_y = window_h//2-page_h//2
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, page_w, page_h))

    # grid rows
    row_num = 16
    row_pad_y = page_h*0.1
    row_h = (page_h - row_pad_y*2) / row_num

    for i in range(row_num + 1):
        x_1 = page_x
        y_1 = page_y + row_h * i + row_pad_y
        x_2 = page_x + page_w
        y_2 = page_y + row_h * i + row_pad_y
        pygame.draw.line(screen, '#ff00ff', (x_1, int(y_1)), (x_2, int(y_2)), 1)

    # grid rows
    col_num = 3
    col_pad_x = page_w*0.1
    col_w = (page_w - col_pad_x*2) / col_num

    for i in range(col_num + 1):
        x_1 = page_x + col_w * i + col_pad_x
        y_1 = page_y
        x_2 = page_x + col_w * i + col_pad_x
        y_2 = page_y + page_h
        pygame.draw.line(screen, '#ff00ff', (int(x_1), y_1), (int(x_2), y_2), 1)

    pygame.display.update()