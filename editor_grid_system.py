import random

from lorem_text import lorem
import pygame
from PIL import Image, ImageDraw, ImageFont

import util

vault_folderpath = '/home/ubuntu/vault'

body_text = lorem.words(800)
a4_body_font_size = 28
a4_body_line_spacing = 1.1
a4_body_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica.ttf', a4_body_font_size)

a4_w = 2480
a4_h = 3508

a4_ml = 300
a4_mt = 500
a4_mr = 500
a4_mb = 800

a4_text_area_x1 = a4_ml
a4_text_area_y1 = a4_mt
a4_text_area_x2 = a4_w - a4_mr
a4_text_area_y2 = a4_h - a4_mb
a4_text_area_w = a4_text_area_x2 - a4_text_area_x1
a4_text_area_h = a4_text_area_y2 - a4_text_area_y1

a4_col_num = 2
a4_col_w = a4_text_area_w / a4_col_num
a4_col_gap = a4_body_font_size * 2

a4_row_num = 4
a4_row_h = a4_text_area_h / a4_row_num
a4_row_gap = a4_body_font_size

'''
window_w = 1600
window_h = 900

canvas_w = a4_w // 4
canvas_h = a4_h // 4

canvas_x = window_w // 2 - canvas_w // 2
canvas_y = window_h // 2 - canvas_h // 2

canvas_ml = 30*2
canvas_mt = 50*2
canvas_mr = 50*2
canvas_mb = 80*2

text_area_x = canvas_x + canvas_ml
text_area_y = canvas_y + canvas_mt
text_area_w = canvas_w - canvas_ml - canvas_mr
text_area_h = canvas_h - canvas_mt - canvas_mb

'''

map_matrix = []
for i in range(a4_row_num):
    row = []
    for j in range(a4_col_num):
        row.append('')
    map_matrix.append(row)

def draw_guides(draw):
    x1 = a4_text_area_x1
    y1 = a4_text_area_y1
    x2 = a4_text_area_x2
    y2 = y1
    draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
    x1 = a4_text_area_x1
    y1 = a4_text_area_y2
    x2 = a4_text_area_x2
    y2 = y1
    draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
    x1 = a4_text_area_x1
    y1 = a4_text_area_y1
    x2 = x1
    y2 = a4_text_area_y2
    draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
    x1 = a4_text_area_x2
    y1 = a4_text_area_y1
    x2 = x1
    y2 = a4_text_area_y2
    draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
    for i in range(a4_col_num+1):
        if i == 0: continue
        x1 = a4_text_area_x1 + a4_col_w*i
        y1 = a4_text_area_y1
        x2 = x1
        y2 = a4_text_area_y2
        draw.line((x1, y1, x2, y2), fill='#00ffff', width=4)
        draw.line((x1 - a4_col_gap, y1, x2 - a4_col_gap, y2), fill='#00ffff', width=4)
    for i in range(a4_row_num+1):
        if i == 0: continue
        x1 = a4_text_area_x1
        y1 = a4_text_area_y1 + a4_row_h*i
        x2 = a4_text_area_x2 
        y2 = y1
        draw.line((x1, y1, x2, y2), fill='#00ffff', width=4)
        draw.line((x1, y1 - a4_row_gap, x2, y2 - a4_row_gap), fill='#00ffff', width=4)
    

def magazine_gen(image_i):
    for i in range(a4_row_num):
        for j in range(a4_col_num):
            map_matrix[i][j] = ''

    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)

    draw_guides(draw)

    ## images
    foreground = Image.open('image-test.png')
    cell_x1_index = random.randint(0, a4_col_num-1)
    cell_y1_index = random.randint(0, a4_row_num-1)
    cell_x2_index = random.randint(cell_x1_index, a4_col_num-1)
    cell_y2_index = random.randint(cell_y1_index, a4_row_num-1)
    print(f'{cell_x1_index}:{cell_y1_index}')
    print(f'{cell_x2_index}:{cell_y2_index}')
    print()
    for i in range(a4_row_num):
        for j in range(a4_col_num):
            if i >= cell_y1_index and j >= cell_x1_index and i <= cell_y2_index and j <= cell_x2_index:
                map_matrix[i][j] = 'i_0'

    for row in map_matrix:
        print(row)
    
    x1 = int(a4_ml + a4_col_w * cell_x1_index)
    y1 = int(a4_mt + a4_row_h * cell_y1_index)
    w = int(a4_col_w * (cell_x2_index - cell_x1_index + 1) - a4_col_gap)
    h = int(a4_row_h * (cell_y2_index - cell_y1_index + 1) - a4_row_gap)

    util.img_resize_save(
        'image-test.png', 'image-test-resized.jpg', 
        w=w, h=h, 
        quality=100,
    )
    foreground = Image.open('image-test-resized.jpg')
    img.paste(foreground, (x1, y1))

    ## body
    lines = []
    line_curr = ''
    for word in body_text.split(' '):
        _, _, line_curr_w, _ = a4_body_font.getbbox(line_curr)
        _, _, word_w, _ = a4_body_font.getbbox(word)
        if line_curr_w + word_w < a4_col_w - a4_col_gap:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr.strip())

    blocks = []
    for i in range(a4_col_num):
        for j in range(a4_row_num):
            print(f'col: {i}, row: {j} - {map_matrix[j][i]}')
            if map_matrix[j][i] == '':
                blocks.append([i, j])
    print(blocks)
    
    if len(blocks) != 0:
        block_index = 0
        block_curr_x, block_curr_y = blocks[block_index]
        i = 0
        for line in lines:
            x1 = a4_ml + a4_col_w*block_curr_x
            y1 = a4_mt + a4_row_h*block_curr_y
            y_line = y1 + (a4_body_font_size*i*a4_body_line_spacing)
            if block_index+1 < len(blocks):
                if blocks[block_index+1][1] - block_curr_y != 1:
                    block_h = a4_row_h - a4_body_font_size*a4_body_line_spacing
                else:
                    block_h = a4_row_h
            else:
                ## if last block of column
                block_h = a4_row_h - a4_body_font_size*a4_body_line_spacing

            if y_line - y1 >= block_h:
                block_index += 1
                i = 0
                if block_index >= len(blocks): break
                block_curr_x, block_curr_y = blocks[block_index]
                x1 = a4_ml + a4_col_w*block_curr_x
                y1 = a4_mt + a4_row_h*block_curr_y
                y_line = y1 + (a4_body_font_size*i*a4_body_line_spacing)
            draw.text((x1, y_line), line, '#000000', font=a4_body_font)
            i += 1

    '''
    ## check avg words per line
    words_sum = len(body_text.split(' '))
    avg_len = words_sum / len(lines)
    print(avg_len)
    '''

    img.save(f'exports-test/{image_i}.jpg')
    # img.show()


for image_i in range(100):
    magazine_gen(image_i)

quit()

pygame.init()
pygame.display.set_caption("Magazine Editor")
screen = pygame.display.set_mode((window_w, window_h), 0, 32)
font_1 = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 32)

font_body_size = 12
font_body_line_spacing = 1.1
font_body = pygame.font.SysFont(f'{vault_folderpath}/fonts/helvetica/Helvetica.ttf', font_body_size)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                 magazine_gen()

    ## background
    pygame.draw.rect(screen, '#111111', (0, 0, window_w, window_h))

    ## canvas
    pygame.draw.rect(screen, '#ffffff', (canvas_x, canvas_y, canvas_w, canvas_h))

    ## guides text area
    color = '#ff0000'
    ## left
    x1 = canvas_x + canvas_ml
    y1 = canvas_y + canvas_mt
    x2 = x1
    y2 = canvas_y + canvas_h - canvas_mb
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
    ## top
    x1 = canvas_x + canvas_ml
    y1 = canvas_y + canvas_mt
    x2 = canvas_x + canvas_w - canvas_mr
    y2 = y1
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
    ## right
    x1 = canvas_x + canvas_w - canvas_mr
    y1 = canvas_y + canvas_mt
    x2 = x1
    y2 = canvas_y + canvas_h - canvas_mb
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
    ## bottom
    x1 = canvas_x + canvas_ml
    y1 = canvas_y + canvas_h - canvas_mb
    x2 = canvas_x + canvas_w - canvas_mr
    y2 = y1
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

    ## guides cols
    color = '#00ffff'
    col_num = 2
    col_gap = 10
    col_w = text_area_w // col_num
    for i in range(col_num+1):
        if i == 0: continue
        x1 = text_area_x + col_w*i
        y1 = canvas_y + canvas_mt
        x2 = x1
        y2 = canvas_y + canvas_h - canvas_mb
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
        pygame.draw.line(screen, color, (x1 - col_gap, y1), (x2 - col_gap, y2), 2)

    ## guides rows
    color = '#00ffff'
    row_num = 8
    row_gap = 10
    row_h = text_area_h // row_num
    for i in range(row_num+1):
        if i == 0: continue
        x1 = text_area_x
        y1 = text_area_y + row_h*i
        x2 = text_area_x + text_area_w
        y2 = y1
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
        pygame.draw.line(screen, color, (x1, y1 - row_gap), (x2, y2 - row_gap), 2)

    ## draw text
    lines = []
    line_curr = ''
    for word in body_text.split(' '):
        word_w, word_h = font_body.size(word)
        line_curr_w, line_curr_h = font_body.size(line_curr)
        if line_curr_w + word_w < col_w - col_gap:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr.strip())
    line_h_max = 0
    for line in lines:
        line_w, line_h = font_body.size(line)
        if line_h_max < line_h:
            line_h_max = line_h
    i = 0
    for line in lines:
        text_surface = font_body.render(line, False, '#000000')
        screen.blit(text_surface, (text_area_x, text_area_y + line_h*i*font_body_line_spacing))
        i += 1

        

    '''
    line_width, line_height = font_body.size(body_text)
    text_surface = font_body.render(body_text, False, '#000000')
    screen.blit(text_surface, (text_area_x, text_area_y))
    '''

    pygame.display.flip()

