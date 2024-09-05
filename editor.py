import os

import pygame
from PIL import Image, ImageDraw, ImageFont

from oliark import file_read
from oliark import img_resize_save

A4_WIDTH = 2480 * 2
A4_HEIGHT = 3508

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1280

CANVAS_WIDTH = A4_WIDTH//4
CANVAS_HEIGHT = A4_HEIGHT//4

canvas_x = WINDOW_WIDTH//2 - CANVAS_WIDTH//2
canvas_y = WINDOW_HEIGHT//2 - CANVAS_HEIGHT//2

cols_num = 22
rows_num = 16
cols_width = CANVAS_WIDTH / cols_num
rows_height = CANVAS_HEIGHT / rows_num

cols_gap = cols_width//4

body_font_size = 14

pygame.init()
pygame.display.set_caption("Magazine Editor")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 14)

grid_show = True

img_resize_save('image-test.png', 'image-test-resized.jpg', w=CANVAS_WIDTH//2+cols_width*3, h=CANVAS_HEIGHT, quality=100)
image_test = pygame.image.load('image-test-resized.jpg')

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_show = not grid_show

    ## background
    pygame.draw.rect(screen, '#111111', (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    ## canvas
    pygame.draw.rect(screen, '#ffffff', (canvas_x, canvas_y, CANVAS_WIDTH, CANVAS_HEIGHT))

    ## image
    screen.blit(image_test, (canvas_x + CANVAS_WIDTH//2 - cols_width*3, canvas_y))

    ## text
    content = file_read('body-test.txt')
    content = content.strip().replace('\n', ' ').replace('   ', ' ').replace('  ', ' ')
    lines = []
    line_curr = ''
    for word in content.split(' '):
        word_width, word_height = my_font.size(word)
        line_curr_width, line_curr_height = my_font.size(line_curr)
        if line_curr_width + word_width < cols_width*3 - cols_gap:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr.strip())

    line_height_max = 0
    for line in lines:
        line_width, line_height = my_font.size(line)
        if line_height_max < line_height:
            line_height_max = line_height

    line_spacing = 1.2
    for line_i, line in enumerate(lines):
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#000000')
        line_x = canvas_x + cols_width*1
        line_y = canvas_y + rows_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - rows_height*2:
            screen.blit(text_surface, (line_x, line_y))
    for line_i, line in enumerate(lines):
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#000000')
        line_x = canvas_x + cols_width*4
        line_y = canvas_y + rows_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - rows_height*2:
            screen.blit(text_surface, (line_x, line_y))

    if grid_show:
        ## grid
        for i in range(cols_num+1):
            pygame.draw.line(screen, '#333333', (canvas_x + int(cols_width*i), 0), (canvas_x + int(cols_width*i), WINDOW_HEIGHT), 1)
        for i in range(rows_num+1):
            pygame.draw.line(screen, '#333333', (0, canvas_y + int(rows_height*i)), (WINDOW_WIDTH, canvas_y + int(rows_height*i)), 1)
        
        ## guides
        pygame.draw.line(screen, '#00ffff', (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT), 2)

    pygame.display.flip()
