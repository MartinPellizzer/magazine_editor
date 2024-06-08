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


row_num = 16
row_pad_y = page_h*0.1
row_h = (page_h - row_pad_y*2) / row_num

col_num = 3
col_pad_x = page_w*0.1
col_w = (page_w - col_pad_x*2) / col_num

grid = []
for row_i in range(row_num):
    row_curr = []
    for col_i in range(col_num):
        row_curr.append(0)
    grid.append(row_curr)

screen = pygame.display.set_mode((window_w, window_h), 0, 32)

pygame.display.set_caption("Magazine Editor")

background = pygame.image.load(background_image).convert()
mouse_cursor = pygame.image.load(mouse_image).convert()
my_font = pygame.font.SysFont('assets/fonts/arial/ARIAL.TTF', 30)

def cell_from_pos(pos):
    col_i = int((x_1 - col_pad_x - page_x) // col_w)
    row_i = int((y_1 - row_pad_y - page_y) // row_h)
    return col_i, row_i


mouse_click_col_i = 0
mouse_click_row_i = 0
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_pos = pygame.mouse.get_pos()
            mouse_click_col_i, mouse_click_row_i = cell_from_pos(mouse_click_pos)
            grid[mouse_click_row_i][mouse_click_col_i] = 1
            print(grid)

    
    # draw window bg
    pygame.draw.rect(screen, '#000000', (0, 0, page_w, page_h))
    
    # draw page
    page_x = window_w//2-page_w//2
    page_y = window_h//2-page_h//2
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, page_w, page_h))

    # grid rows
    for i in range(row_num + 1):
        x_1 = page_x
        y_1 = page_y + row_h * i + row_pad_y
        x_2 = page_x + page_w
        y_2 = page_y + row_h * i + row_pad_y
        pygame.draw.line(screen, '#ff00ff', (x_1, int(y_1)), (x_2, int(y_2)), 1)

    # grid rows
    for i in range(col_num + 1):
        x_1 = page_x + col_w * i + col_pad_x
        y_1 = page_y
        x_2 = page_x + col_w * i + col_pad_x
        y_2 = page_y + page_h
        pygame.draw.line(screen, '#ff00ff', (int(x_1), y_1), (int(x_2), y_2), 1)

    for col_i in range(col_num):
        for row_i in range(row_num):
            x_1 = page_x + col_w * col_i + col_pad_x
            y_1 = page_y + row_h * row_i + row_pad_y
            text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
            screen.blit(text_surface, (x_1, y_1))

    # mouse coord - abs
    x_1, y_1 = pygame.mouse.get_pos()    
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 0))

    # mouse coord - page
    x_1, y_1 = pygame.mouse.get_pos()
    x_1 = x_1 - page_x
    y_1 = y_1 - page_y
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 30))

    # mouse coord - cell index
    x_1, y_1 = pygame.mouse.get_pos()
    col_i = int((x_1 - col_pad_x - page_x) // col_w)
    row_i = int((y_1 - row_pad_y - page_y) // row_h)
    text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 60))

    # mouse coord - cell clicked index
    text_surface = my_font.render(f'{mouse_click_col_i}:{mouse_click_row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 90))

    
    for row_i in range(row_num):
        for col_i in range(col_num):
            if grid[row_i][col_i] == 1:
                red_x_1 = page_x + col_w * col_i + col_pad_x
                red_y_1 = page_y + row_h * row_i + row_pad_y
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, 10, 10))

    pygame.display.update()