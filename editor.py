import os

import pygame
from PIL import Image, ImageDraw, ImageFont

import util

A4_WIDTH = 2480 * 2
A4_HEIGHT = 3508

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

CANVAS_WIDTH = A4_WIDTH//4
CANVAS_HEIGHT = A4_HEIGHT//4

canvas_x = WINDOW_WIDTH//2 - CANVAS_WIDTH//2
canvas_y = WINDOW_HEIGHT//2 - CANVAS_HEIGHT//2

cols_num = 64
rows_num = int(cols_num*1.41/2)

col_width = CANVAS_WIDTH / cols_num
row_height = CANVAS_HEIGHT / rows_num

print(col_width)
print(row_height)

cols_gap = col_width//4

p1_margin_left = col_width*3
p1_margin_right = col_width*5

print_area_w = CANVAS_WIDTH//2 - p1_margin_left - p1_margin_right
print(CANVAS_WIDTH)
print(print_area_w)
# quit()

grid_map = []
for row_i in range(rows_num):
    row_curr = []
    for col_i in range(cols_num):
        row_curr.append('')
    grid_map.append(row_curr)

body_font_size = 14

pygame.init()
pygame.display.set_caption("Magazine Editor")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 14)

grid_show = True

util.img_resize_save('image-test.png', 'image-test-resized.jpg', w=CANVAS_WIDTH//2+col_width*3, h=CANVAS_HEIGHT, quality=100)
image_test = pygame.image.load('image-test-resized.jpg')

def grid_map_copy():
    tmp = []
    for row_i in range(rows_num):
        row_curr = []
        for col_i in range(cols_num):
            row_curr.append(grid_map[row_i][col_i])
        tmp.append(row_curr)
    return tmp

tmp_grid_map = grid_map_copy()

flag_brush_type = 'i'
flag_image_num = 0

drag_x_1 = -1
drag_y_1 = -1

flag_preview = True

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_show = not grid_show
            if event.key == pygame.K_SPACE:
                if flag_brush_type == 'i': flag_brush_type = 'p'
                elif flag_brush_type == 'p': flag_brush_type = 'i'
            if event.key == pygame.K_p:
                flag_preview = not flag_preview
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag_drag = True
            pos = pygame.mouse.get_pos()
            drag_x_1 = pos[0]
            drag_y_1 = pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            flag_drag = False
            grid_map = tmp_grid_map

        if pygame.mouse.get_pressed()[0]:
            tmp_grid_map = grid_map_copy()
            
            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - canvas_x) // col_width)
            drag_r_1 = int((drag_y_1 - canvas_y) // row_height)
            drag_c_2 = int((drag_x_2 - canvas_x) // col_width)
            drag_r_2 = int((drag_y_2 - canvas_y) // row_height)

            for row_i in range(rows_num):
                for col_i in range(cols_num):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):
                        
                        if flag_brush_type == 'i' and flag_image_num == 0:
                            if 'i_0' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_0'
                        if flag_brush_type == 'p':
                            if 'p' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 'p'

    ## background
    pygame.draw.rect(screen, '#111111', (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    ## canvas
    pygame.draw.rect(screen, '#ffffff', (canvas_x, canvas_y, CANVAS_WIDTH, CANVAS_HEIGHT))

    ## image
    if flag_preview:
        screen.blit(image_test, (canvas_x + CANVAS_WIDTH//2 - col_width*3, canvas_y))

    ## text
    with open('body-test.txt') as f: content = f.read()
    content = content.strip().replace('\n', ' ').replace('   ', ' ').replace('  ', ' ')
    lines = []
    line_curr = ''
    for word in content.split(' '):
        word_width, word_height = my_font.size(word)
        line_curr_width, line_curr_height = my_font.size(line_curr)
        if line_curr_width + word_width < col_width*3 - cols_gap:
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
        line_x = canvas_x + col_width*1
        line_y = canvas_y + row_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - row_height*2:
            screen.blit(text_surface, (line_x, line_y))
    for line_i, line in enumerate(lines):
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#000000')
        line_x = canvas_x + col_width*4
        line_y = canvas_y + row_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - row_height*2:
            screen.blit(text_surface, (line_x, line_y))

    if grid_show:
        ## grid
        for i in range(cols_num+1):
            pygame.draw.line(screen, '#333333', (canvas_x + int(col_width*i), 0), (canvas_x + int(col_width*i), WINDOW_HEIGHT), 1)
        for i in range(rows_num+1):
            pygame.draw.line(screen, '#333333', (0, canvas_y + int(row_height*i)), (WINDOW_WIDTH, canvas_y + int(row_height*i)), 1)
        
    ## inner_cols
    inner_cols_num = 9
    inner_col_w = print_area_w / inner_cols_num
    for i in range(inner_cols_num+1):
        x1 = int(canvas_x + p1_margin_left + inner_col_w*i)
        y1 = int(canvas_y)
        x2 = int(canvas_x + p1_margin_left + inner_col_w*i)
        y2 = int(canvas_y + CANVAS_HEIGHT)
        pygame.draw.line(screen, '#00ffff', (x1, y1), (x2, y2), 2)

    ## guides
    # pygame.draw.line(screen, '#000000', (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, '#000000', (canvas_x + CANVAS_WIDTH//2, 0), (canvas_x + CANVAS_WIDTH//2, WINDOW_HEIGHT), 2)

    ## margins
    x1 = canvas_x + p1_margin_left
    y1 = canvas_y
    x2 = canvas_x + p1_margin_left
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)
    
    x1 = canvas_x + CANVAS_WIDTH//2 - p1_margin_right
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH//2 - p1_margin_right
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x + CANVAS_WIDTH//2 + col_width*5
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH//2 + col_width*5
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x + CANVAS_WIDTH - col_width*3
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH - col_width*3
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x
    y1 = canvas_y + row_height*5
    x2 = canvas_x + CANVAS_WIDTH
    y2 = canvas_y + row_height*5
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x
    y1 = canvas_y + CANVAS_HEIGHT - row_height*8
    x2 = canvas_x + CANVAS_WIDTH
    y2 = canvas_y + CANVAS_HEIGHT - row_height*8
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    ## blocks colors
    for row_i in range(rows_num):
        for col_i in range(cols_num):
            if 'i_0' in tmp_grid_map[row_i][col_i]:
                red_x_1 = canvas_x + col_width * col_i
                red_y_1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, col_width, row_height))
            
            if 'p' in tmp_grid_map[row_i][col_i]:
                x1 = canvas_x + col_width * col_i
                y1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#000000', (x1, y1, col_width, row_height))

    if 'debug':
        line_x = 0
        line_y = 0

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        line = f'x: {x} - y: {y}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16

        x = pos[0] - canvas_x
        y = pos[1] - canvas_y
        line = f'x: {x} - y: {y}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16
        
        col_i = int(x//col_width) 
        row_i = int(y//row_height)
        line = f'col_i: {col_i} - row_i: {row_i}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16
        
        line = f'flag_brush_type: {flag_brush_type}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16


    pygame.display.flip()
