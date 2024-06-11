import pygame
from pygame.locals import *
from sys import exit

import os
import csv
from PIL import Image, ImageDraw, ImageFont
import random

import util
import os






####################################################################################################
# VAR
####################################################################################################
c_grid = '#cdcdcd'

body_font_size = 30
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", body_font_size)

a4_w = 2480
a4_h = 3508

window_w = 1280
window_h = 720

page_w = 248*2
page_h = 351*2
page_x = window_w//2-page_w//2
page_y = window_h//2-page_h//2

# FLAGS
flag_a4_grid = 1
flag_brush_type = 't'


mouse_click_col_i = 0
mouse_click_row_i = 0
show_grid = 1

# GRID
page_grid_col_num = 16 
page_grid_col_w = page_w / page_grid_col_num

page_grid_row_num = 16 
page_grid_row_h = page_h / page_grid_row_num

page_guides_col_num = 2
page_guides_col_padding = page_grid_col_w*4
page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num

page_guides_row_num = 12
page_guides_row_padding = page_grid_row_h*4
page_guides_row_h = (page_h - page_guides_row_padding) / page_guides_row_num

grid_map = []
for row_i in range(page_grid_row_num):
    row_curr = []
    for col_i in range(page_grid_col_num):
        row_curr.append('')
    grid_map.append(row_curr)




# PYGAME
pygame.init()

screen = pygame.display.set_mode((window_w, window_h), 0, 32)

pygame.display.set_caption("Magazine Editor")
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 30)



while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
                
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            mouse_click_col_i = int((x - page_x) // page_grid_col_w)
            mouse_click_row_i = int((y - page_y) // page_grid_row_h)
            if flag_brush_type == 't':
                if (mouse_click_row_i >= 0 and 
                    mouse_click_row_i < page_grid_row_num and 
                    mouse_click_col_i >= 0 and 
                    mouse_click_col_i < page_grid_col_num):
                    grid_map[mouse_click_row_i][mouse_click_col_i] = 't'
            if flag_brush_type == 'b':
                if (mouse_click_row_i >= 0 and 
                    mouse_click_row_i < page_grid_row_num and 
                    mouse_click_col_i >= 0 and 
                    mouse_click_col_i < page_grid_col_num):
                    grid_map[mouse_click_row_i][mouse_click_col_i] = 'b'
            if flag_brush_type == 'i':
                if (mouse_click_row_i >= 0 and 
                    mouse_click_row_i < page_grid_row_num and 
                    mouse_click_col_i >= 0 and 
                    mouse_click_col_i < page_grid_col_num):
                    grid_map[mouse_click_row_i][mouse_click_col_i] = 'i'
            print(grid_map)

        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            mouse_click_col_i = int((x - page_x) // page_grid_col_w)
            mouse_click_row_i = int((y - page_y) // page_grid_row_h)
            grid_map[mouse_click_row_i][mouse_click_col_i] = ''

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print('1')
                page_guides_col_num = 1
                page_guides_col_padding = page_grid_col_w*4
                page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num
            if event.key == pygame.K_2:
                page_guides_col_num = 2
                page_guides_col_padding = page_grid_col_w*4
                page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num
                print('2')
            if event.key == pygame.K_3:
                page_guides_col_num = 3
                page_guides_col_padding = page_grid_col_w*4
                page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num
                print('3')
            if event.key == pygame.K_SPACE:
                if flag_brush_type == 't': flag_brush_type = 'b'
                elif flag_brush_type == 'b': flag_brush_type = 'i'
                elif flag_brush_type == 'i': flag_brush_type = 't'
                
    # draw window bg
    pygame.draw.rect(screen, '#000000', (0, 0, page_w, page_h))

    # draw page bg
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, page_w, page_h))

    for i in range(page_grid_col_num + 1):
        x_1 = page_x + page_grid_col_w * i
        y_1 = page_y
        x_2 = page_x + page_grid_col_w * i
        y_2 = page_y + page_h
        pygame.draw.line(screen, c_grid, (int(x_1), y_1), (int(x_2), y_2), 1)
    for i in range(page_grid_row_num + 1):
        x_1 = page_x
        y_1 = page_y + page_grid_row_h * i
        x_2 = page_x + page_w
        y_2 = page_y + page_grid_row_h * i
        pygame.draw.line(screen, c_grid, (x_1, int(y_1)), (x_2, int(y_2)), 1)

    for i in range(page_guides_col_num + 1):
        x_1 = page_x + page_guides_col_w * i + page_guides_col_padding//2
        y_1 = page_y
        x_2 = page_x + page_guides_col_w * i + page_guides_col_padding//2
        y_2 = page_y + page_h
        pygame.draw.line(screen, '#ff00ff', (int(x_1), y_1), (int(x_2), y_2), 1)
    for i in range(page_guides_row_num + 1):
        x_1 = page_x
        y_1 = page_y + page_guides_row_h * i + page_guides_row_padding//2
        x_2 = page_x + page_w
        y_2 = page_y + page_guides_row_h * i + page_guides_row_padding//2
        pygame.draw.line(screen, '#ff00ff', (x_1, int(y_1)), (x_2, int(y_2)), 1)

    # draw_mouse_pos_abs()
    x_1, y_1 = pygame.mouse.get_pos()    
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 0))
    
    # draw_mouse_pos_page()
    x_1, y_1 = pygame.mouse.get_pos()
    x_1 = x_1 - page_x
    y_1 = y_1 - page_y
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 30))

    # draw_mouse_pos_cell()
    x_1, y_1 = pygame.mouse.get_pos()
    col_i = int((x_1 - page_x) // page_grid_col_w)
    row_i = int((y_1 - page_y) // page_grid_row_h)
    text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 60))

    # mouse coord - cell clicked index
    text_surface = my_font.render(f'{mouse_click_col_i}:{mouse_click_row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 90))
    
    # flags
    text_surface = my_font.render(f'flag_a4_grid:{flag_a4_grid}', False, '#ff00ff')
    screen.blit(text_surface, (0, 120))
    text_surface = my_font.render(f'flag_brush_type:{flag_brush_type}', False, '#ff00ff')
    screen.blit(text_surface, (0, 150))

    
    for row_i in range(page_grid_row_num):
        for col_i in range(page_grid_col_num):
            if grid_map[row_i][col_i] == 't':
                red_x_1 = page_x + page_grid_col_w * col_i
                red_y_1 = page_y + page_grid_row_h * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, page_grid_col_w, page_grid_row_h))
            if grid_map[row_i][col_i] == 'b':
                red_x_1 = page_x + page_grid_col_w * col_i
                red_y_1 = page_y + page_grid_row_h * row_i
                pygame.draw.rect(screen, '#000000', (red_x_1, red_y_1, page_grid_col_w, page_grid_row_h))
            if grid_map[row_i][col_i] == 'i':
                red_x_1 = page_x + page_grid_col_w * col_i
                red_y_1 = page_y + page_grid_row_h * row_i
                pygame.draw.rect(screen, '#0000ff', (red_x_1, red_y_1, page_grid_col_w, page_grid_row_h))

    pygame.display.update()