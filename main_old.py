import pygame
from pygame.locals import *
from sys import exit

import os
import csv
from PIL import Image, ImageDraw, ImageFont
import random

import requests


def img_resize(img, w, h):
    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    return img


def unsplash_image_get():
    with open('C:/api-keys/unsplash-api-key.txt', 'r') as f:
        ACCESS_KEY = f.read().strip()

    url = f'https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}'
    url = f'https://api.unsplash.com/search/photos?page=1&query=travel&client_id={ACCESS_KEY}'
    response = requests.get(url)
    print(response)

    data = response.json()['results']
    random_image = random.choice(data)

    filename = 'picture.jpg'
    image_url = random_image['urls']['regular']
    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in image_response:
                f.write(chunk)

    print(image_url)


c_grid = '#cdcdcd'


body_font_size = 30
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", body_font_size)


background_image = 'assets/bg-image.jpg'
mouse_image = 'assets/bg-image.jpg'

pygame.init()

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




row_num = 16
row_pad_y = page_h*0.1
grid_col_gap = 16
row_h = (page_h - row_pad_y*2) / row_num

col_num = 3
col_pad_x = page_w*0.1
col_w = (page_w - col_pad_x*2) / col_num

grid = []
for row_i in range(row_num):
    row_curr = []
    for col_i in range(col_num):
        row_curr.append('')
    grid.append(row_curr)

screen = pygame.display.set_mode((window_w, window_h), 0, 32)

pygame.display.set_caption("Magazine Editor")

background = pygame.image.load(background_image).convert()
mouse_cursor = pygame.image.load(mouse_image).convert()
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 30)


def cell_from_pos(pos):
    x = pos[0]
    y = pos[1]
    col_i = int((x - col_pad_x - page_x) // col_w)
    row_i = int((y - row_pad_y - page_y) // row_h)
    return col_i, row_i


def draw_background():
    pygame.draw.rect(screen, '#000000', (0, 0, page_w, page_h))


def draw_page():
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, page_w, page_h))


def draw_grid_lines():
    for i in range(row_num + 1):
        x_1 = page_x
        y_1 = page_y + row_h * i + row_pad_y
        x_2 = page_x + page_w
        y_2 = page_y + row_h * i + row_pad_y
        pygame.draw.line(screen, '#ff00ff', (x_1, int(y_1)), (x_2, int(y_2)), 1)

    for i in range(col_num + 1):
        x_1 = page_x + col_w * i + col_pad_x
        y_1 = page_y
        x_2 = page_x + col_w * i + col_pad_x
        y_2 = page_y + page_h
        pygame.draw.line(screen, '#ff00ff', (int(x_1), y_1), (int(x_2), y_2), 1)


def draw_grid_cell_num():
    for col_i in range(col_num):
        for row_i in range(row_num):
            x_1 = page_x + col_w * col_i + col_pad_x
            y_1 = page_y + row_h * row_i + row_pad_y
            text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
            screen.blit(text_surface, (x_1, y_1))


def draw_mouse_pos_abs():
    x_1, y_1 = pygame.mouse.get_pos()    
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 0))


def draw_mouse_pos_page():
    x_1, y_1 = pygame.mouse.get_pos()
    x_1 = x_1 - page_x
    y_1 = y_1 - page_y
    text_surface = my_font.render(f'{x_1}:{y_1}', False, '#ff00ff')
    screen.blit(text_surface, (0, 30))


def draw_mouse_pos_cell():
    x_1, y_1 = pygame.mouse.get_pos()
    col_i = int((x_1 - col_pad_x - page_x) // col_w)
    row_i = int((y_1 - row_pad_y - page_y) // row_h)
    text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 60))


#########################################################
# PDF
#########################################################

def preview_page():
    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)

    # grid
    pdf_grid_col_num = 3
    pdf_col_pad_x = 256
    pdf_grid_col_gap = 16
    pdf_col_w = (a4_w - pdf_col_pad_x*2) // pdf_grid_col_num

    pdf_grid_row_num = 16
    pdf_row_pad_y = 512
    pdf_row_h = (a4_h - pdf_row_pad_y*2) // pdf_grid_row_num
    
    if flag_a4_grid:
        # draw grid cols
        for i in range(pdf_grid_col_num+1):
            x_1 = pdf_col_w*i + pdf_col_pad_x
            y_1 = 0
            x_2 = pdf_col_w*i + pdf_col_pad_x
            y_2 = a4_h
            draw.line((x_1, y_1, x_2, y_2), fill='#ff00ff', width=4)
            draw.line((pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)
            draw.line((pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)

        # draw grid rows
        for i in range(pdf_grid_row_num+1):
            x_1 = 0
            y_1 = pdf_row_h*i + pdf_row_pad_y
            x_2 = a4_w
            y_2 = pdf_row_h*i + pdf_row_pad_y
            draw.line((x_1, y_1, x_2, y_2), fill='#ff00ff', width=4)

    # draw image
    col_i_x_1 = ''
    col_i_y_1 = ''
    col_i_x_2 = ''
    col_i_y_2 = ''
    is_first_pos = True
    for row_i in range(row_num):
        for col_i in range(col_num):
            if grid[row_i][col_i] == 'i':
                if is_first_pos: 
                    col_i_x_1 = col_i
                    col_i_y_1 = row_i
                    is_first_pos = False
                else:
                    col_i_x_2 = col_i
                    col_i_y_2 = row_i

    if col_i_x_1 != '':
        x_1 = pdf_col_w * col_i_x_1 + pdf_col_pad_x
        y_1 = pdf_row_h * col_i_y_1 + pdf_row_pad_y
        x_2 = pdf_col_w * (col_i_x_2 + 1) + pdf_col_pad_x
        y_2 = pdf_row_h * (col_i_y_2 + 1) + pdf_row_pad_y
        draw.rectangle(((x_1, y_1), (x_2, y_2)), fill="#cdcdcd")

        foreground = Image.open("picture.jpg")
        fg_w = x_2 - x_1
        fg_h = y_2 - y_1
        foreground = img_resize(foreground, fg_w, fg_h)
        img.paste(foreground, (x_1, y_1))

    
    with open('placeholder_text.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
    text = text.replace('\n', ' ')

    
    # draw text
    # col_i_x_1 = ''
    # col_i_y_1 = ''
    # col_i_x_2 = ''
    # col_i_y_2 = ''
    # is_first_pos = True
    # for row_i in range(row_num):
    #     for col_i in range(col_num):
    #         if grid[row_i][col_i] == 't':
    #             if is_first_pos: 
    #                 col_i_x_1 = col_i
    #                 col_i_y_1 = row_i
    #                 is_first_pos = False
    #             else:
    #                 col_i_x_2 = col_i
    #                 col_i_y_2 = row_i

    # grid to blocks (text in empty cells)
    # blocks_list = []
    # block_curr = [-1, -1, -1]
    # for k in range(col_num):
    #     for i in range(row_num):
    #         if grid[i][k] == 0:
    #             if block_curr[0] == -1: block_curr[0] = i
    #             if block_curr[1] == -1: block_curr[1] = k
    #         elif grid[i][k] == 1:
    #             if block_curr != [-1, -1, -1]:
    #                 if block_curr[2] == -1: block_curr[2] = i
    #                 blocks_list.append(block_curr)
    #                 block_curr = [-1, -1, -1]
    #     if block_curr != [-1, -1, -1]:
    #         if block_curr[2] == -1: block_curr[2] = i
    #         blocks_list.append(block_curr)
    #         block_curr = [-1, -1, -1]

    blocks_list = []
    block_curr = ['', '', '']
    for col_i in range(col_num):
        for row_i in range(row_num):
            if grid[row_i][col_i] == 't':
                if block_curr[0] == '': block_curr[0] = col_i
                if block_curr[1] == '': block_curr[1] = row_i
            elif grid[row_i][col_i] != 't':
                if block_curr != ['', '', '']:
                    if block_curr[2] == '': block_curr[2] = row_i
                    blocks_list.append(block_curr)
                    block_curr = ['', '', '']
        if block_curr != ['', '', '']:
            if block_curr[2] == '': block_curr[2] = row_i
            blocks_list.append(block_curr)
            block_curr = block_curr = ['', '', '']

    if blocks_list != []:

        # split lines
        words = text.split(' ')
        lines = []
        line_curr = ''
        for word in words:
            _, _, line_curr_w, _ = body_font.getbbox(line_curr)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_curr_w + word_w < pdf_col_w - grid_col_gap*2:
                line_curr += f'{word} '
            else:
                lines.append(line_curr)
                line_curr = f'{word} '
        lines.append(line_curr)

        print(blocks_list)
        # draw text
        block_i = 0
        start_col_i = blocks_list[block_i][0]
        start_row_i = blocks_list[block_i][1]
        end_row_i = blocks_list[block_i][2]
        line_i = 0
        for line in lines:
            x_1 = pdf_col_w * start_col_i + pdf_col_pad_x + grid_col_gap * start_col_i
            y_1 = pdf_row_h * start_row_i + pdf_row_pad_y + body_font_size * line_i
            line_row_i = (y_1 - pdf_row_pad_y) // pdf_row_h
            if line_row_i > end_row_i - 1: 
                print(f'here:{block_i}')
                block_i += 1
                if block_i < len(blocks_list):
                    start_col_i = blocks_list[block_i][0]
                    start_row_i = blocks_list[block_i][1]
                    end_row_i = blocks_list[block_i][2]
                    line_i = 0
                    x_1 = pdf_col_w * start_col_i + pdf_col_pad_x + grid_col_gap * start_col_i
                    y_1 = pdf_row_h * start_row_i + pdf_row_pad_y + body_font_size * line_i
                else:
                    break
            draw.text((x_1, y_1), line, (0, 0, 0), font=body_font)
            line_i += 1

    img.show()



# mouse_click_col_i = 0
# mouse_click_row_i = 0
# show_grid = 1

# while True:
#     for event in pygame.event.get():
#         if event.type==QUIT:
#             exit()
            
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     mouse_click_pos = pygame.mouse.get_pos()
#         #     mouse_click_col_i, mouse_click_row_i = cell_from_pos(mouse_click_pos)
#         #     grid[mouse_click_row_i][mouse_click_col_i] = 1
#         #     print(grid)
            
#         if pygame.mouse.get_pressed()[0]:
#             mouse_click_pos = pygame.mouse.get_pos()
#             mouse_click_col_i, mouse_click_row_i = cell_from_pos(mouse_click_pos)
#             if flag_brush_type == 't':
#                 grid[mouse_click_row_i][mouse_click_col_i] = 't'
#             if flag_brush_type == 'i':
#                 if mouse_click_row_i >= 0 and mouse_click_row_i < row_num and mouse_click_col_i >= 0 and mouse_click_col_i < col_num:
#                     grid[mouse_click_row_i][mouse_click_col_i] = 'i'
#                 else: 
#             print(grid)

#         if pygame.mouse.get_pressed()[2]:
#             mouse_click_pos = pygame.mouse.get_pos()
#             mouse_click_col_i, mouse_click_row_i = cell_from_pos(mouse_click_pos)
#             grid[mouse_click_row_i][mouse_click_col_i] = ''
#             print(grid)
            
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 print('key left')
#             if event.key == pygame.K_RIGHT:
#                 print('key right')
#             if event.key == pygame.K_s:
#                 with open('map.csv', 'w', newline='') as f:
#                     write = csv.writer(f)
#                     write.writerows(grid)
#             # CTRL + G
#             if event.key == pygame.K_g and (pygame.key.get_mods() & pygame.KMOD_CTRL):
#                 flag_a4_grid = not flag_a4_grid
#             # G
#             elif event.key == pygame.K_g:
#                 show_grid = not show_grid
#             if event.key == pygame.K_p:
#                 preview_page()
            
#             if event.key == pygame.K_t:
#                 flag_brush_type = 't'
#             if event.key == pygame.K_i:
#                 flag_brush_type = 'i'
            


#     draw_background()
#     draw_page()

#     if show_grid:
#         draw_grid_lines()
#         draw_grid_cell_num()

#     draw_mouse_pos_abs()
#     draw_mouse_pos_page()
#     draw_mouse_pos_cell()

#     # mouse coord - cell clicked index
#     text_surface = my_font.render(f'{mouse_click_col_i}:{mouse_click_row_i}', False, '#ff00ff')
#     screen.blit(text_surface, (0, 90))
    
#     # flags
#     text_surface = my_font.render(f'flag_a4_grid:{flag_a4_grid}', False, '#ff00ff')
#     screen.blit(text_surface, (0, 120))
#     text_surface = my_font.render(f'flag_brush_type:{flag_brush_type}', False, '#ff00ff')
#     screen.blit(text_surface, (0, 150))

    
#     for row_i in range(row_num):
#         for col_i in range(col_num):
#             if grid[row_i][col_i] == 'i':
#                 red_x_1 = page_x + col_w * col_i + col_pad_x
#                 red_y_1 = page_y + row_h * row_i + row_pad_y
#                 pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, col_w, row_h))
#             if grid[row_i][col_i] == 't':
#                 red_x_1 = page_x + col_w * col_i + col_pad_x
#                 red_y_1 = page_y + row_h * row_i + row_pad_y
#                 pygame.draw.rect(screen, '#000000', (red_x_1, red_y_1, col_w, row_h))

#     pygame.display.update()




mouse_click_col_i = 0
mouse_click_row_i = 0
show_grid = 1

page_grid_col_num = 16 
page_grid_col_w = page_w / page_grid_col_num

page_grid_row_num = 16 
page_grid_row_h = page_h / page_grid_row_num

page_guides_col_num = 3 
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

    

def preview_page_new():
    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)

    if flag_a4_grid:
        a4_grid_col_num = page_grid_col_num
        a4_grid_col_w = a4_w / a4_grid_col_num
        for i in range(a4_grid_col_num+1):
            x_1 = a4_grid_col_w*i
            y_1 = 0
            x_2 = a4_grid_col_w*i
            y_2 = a4_h
            draw.line((x_1, y_1, x_2, y_2), fill='#cdcdcd', width=4)
            # draw.line((pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)
            # draw.line((pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)

        a4_grid_row_num = page_grid_row_num
        a4_grid_row_h = a4_h / a4_grid_row_num
        for i in range(a4_grid_row_num+1):
            x_1 = 0
            y_1 = a4_grid_row_h*i
            x_2 = a4_w
            y_2 = a4_grid_row_h*i
            draw.line((x_1, y_1, x_2, y_2), fill='#cdcdcd', width=4)

        a4_guides_col_num = page_guides_col_num
        a4_guides_col_padding = a4_grid_col_w*4
        a4_guides_col_gap = 16
        a4_guides_col_w = (a4_w - a4_guides_col_padding) / a4_guides_col_num
        for i in range(a4_guides_col_num+1):
            x_1 = a4_guides_col_w*i + a4_guides_col_padding//2
            y_1 = 0
            x_2 = a4_guides_col_w*i + a4_guides_col_padding//2
            y_2 = a4_h
            draw.line((x_1, y_1, x_2, y_2), fill='#ff00ff', width=4)
            # draw.line((pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x - pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)
            # draw.line((pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, 0, pdf_col_w*i + pdf_col_pad_x + pdf_grid_col_gap, a4_h), fill='#ff00ff', width=4)

        a4_guides_row_num = page_guides_row_num
        a4_guides_row_padding = a4_grid_row_h*4
        a4_guides_row_h = (a4_h - a4_guides_row_padding) / a4_guides_row_num
        for i in range(a4_guides_row_num + 1):
            x_1 = 0
            y_1 = a4_guides_row_h*i + a4_guides_row_padding//2
            x_2 = a4_w
            y_2 = a4_guides_row_h*i + a4_guides_row_padding//2
            draw.line((x_1, y_1, x_2, y_2), fill='#ff00ff', width=4)

    # draw image
    col_i_x_1 = ''
    col_i_y_1 = ''
    col_i_x_2 = ''
    col_i_y_2 = ''
    is_first_pos = True
    for row_i in range(a4_grid_row_num):
        for col_i in range(a4_grid_col_num):
            if grid_map[row_i][col_i] == 'i':
                if is_first_pos: 
                    col_i_x_1 = col_i
                    col_i_y_1 = row_i
                    is_first_pos = False
                else:
                    col_i_x_2 = col_i
                    col_i_y_2 = row_i

    if col_i_x_1 != '' and col_i_y_1 != '' and col_i_x_2 != '' and col_i_y_2 != '':
        x_1 = int(a4_grid_col_w * col_i_x_1)
        y_1 = int(a4_grid_row_h * col_i_y_1)
        x_2 = int(a4_grid_col_w * (col_i_x_2 + 1))
        y_2 = int(a4_grid_row_h * (col_i_y_2 + 1))
        draw.rectangle(((x_1, y_1), (x_2, y_2)), fill="#cdcdcd")

        foreground = Image.open("picture.jpg")
        fg_w = x_2 - x_1
        fg_h = y_2 - y_1
        foreground = img_resize(foreground, fg_w, fg_h)
        img.paste(foreground, (x_1, y_1))

    
    with open('placeholder_text.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
    text = text.replace('\n', ' ')

    blocks_list = []
    block_curr = ['', '', '']
    for col_i in range(a4_grid_col_num):
        if col_i == 2 or col_i == 6 or col_i == 10:
            for row_i in range(a4_grid_row_num):
                # print(f'{col_i}:{row_i} -> {grid_map[row_i][col_i]}')
                if grid_map[row_i][col_i] == 't':
                    if block_curr[0] == '': block_curr[0] = col_i
                    if block_curr[1] == '': block_curr[1] = row_i
                elif grid_map[row_i][col_i] != 't':
                    if block_curr != ['', '', '']:
                        if block_curr[2] == '': block_curr[2] = row_i
                        blocks_list.append(block_curr)
                        block_curr = ['', '', '']
            if block_curr != ['', '', '']:
                if block_curr[2] == '': block_curr[2] = row_i
                blocks_list.append(block_curr)
                block_curr = block_curr = ['', '', '']

    if blocks_list != []:
        # split lines
        words = text.split(' ')
        lines = []
        line_curr = ''
        for word in words:
            _, _, line_curr_w, _ = body_font.getbbox(line_curr)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_curr_w + word_w < a4_guides_col_w - a4_guides_col_gap*2:
                line_curr += f'{word} '
            else:
                lines.append(line_curr)
                line_curr = f'{word} '
        lines.append(line_curr)

        print(blocks_list)
        # draw text
        block_i = 0
        start_col_i = blocks_list[block_i][0]
        start_row_i = blocks_list[block_i][1]
        end_row_i = blocks_list[block_i][2]
        line_i = 0
        for line in lines:
            x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
            y_1 = a4_grid_row_h * start_row_i + body_font_size * line_i
            line_row_i = y_1 // a4_guides_row_h
            if line_row_i > end_row_i - 1: 
                print(f'here:{block_i}')
                block_i += 1
                if block_i < len(blocks_list):
                    start_col_i = blocks_list[block_i][0]
                    start_row_i = blocks_list[block_i][1]
                    end_row_i = blocks_list[block_i][2]
                    line_i = 0
                    x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
                    y_1 = a4_grid_row_h * start_row_i + body_font_size * line_i
                else:
                    break
            draw.text((x_1, y_1), line, (0, 0, 0), font=body_font)
            line_i += 1

    img.show()




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
                grid_map[mouse_click_row_i][mouse_click_col_i] = 't'
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
            print(grid_map)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('key left')
            if event.key == pygame.K_RIGHT:
                print('key right')
            if event.key == pygame.K_s:
                with open('map.csv', 'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerows(grid)
            # CTRL + G
            if event.key == pygame.K_g and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                flag_a4_grid = not flag_a4_grid
            # G
            elif event.key == pygame.K_g:
                show_grid = not show_grid

            if event.key == pygame.K_p:
                preview_page_new()
            
            if event.key == pygame.K_t:
                flag_brush_type = 't'
            if event.key == pygame.K_i:
                flag_brush_type = 'i'
            

    draw_background()
    draw_page()

    for i in range(page_grid_col_num + 1):
        x_1 = page_x + page_grid_col_w * i
        y_1 = page_y
        x_2 = page_x + page_grid_col_w * i
        y_2 = page_y + page_h
        pygame.draw.line(screen, c_grid, (int(x_1), y_1), (int(x_2), y_2), 1)

    for i in range(page_guides_col_num + 1):
        x_1 = page_x + page_guides_col_w * i + page_guides_col_padding//2
        y_1 = page_y
        x_2 = page_x + page_guides_col_w * i + page_guides_col_padding//2
        y_2 = page_y + page_h
        pygame.draw.line(screen, '#ff00ff', (int(x_1), y_1), (int(x_2), y_2), 1)


    for i in range(page_grid_row_num + 1):
        x_1 = page_x
        y_1 = page_y + page_grid_row_h * i
        x_2 = page_x + page_w
        y_2 = page_y + page_grid_row_h * i
        pygame.draw.line(screen, c_grid, (x_1, int(y_1)), (x_2, int(y_2)), 1)

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
            if grid_map[row_i][col_i] == 'i':
                red_x_1 = page_x + page_grid_col_w * col_i
                red_y_1 = page_y + page_grid_row_h * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, page_grid_col_w, page_grid_row_h))
            if grid_map[row_i][col_i] == 't':
                red_x_1 = page_x + page_grid_col_w * col_i
                red_y_1 = page_y + page_grid_row_h * row_i
                pygame.draw.rect(screen, '#000000', (red_x_1, red_y_1, page_grid_col_w, page_grid_row_h))

    pygame.display.update()











def draw_body(draw, lines, blocks_list):
    block_i = 0
    start_col_i = blocks_list[block_i][0]
    start_row_i = blocks_list[block_i][1]
    end_row_i = blocks_list[block_i][2]
    line_i = 0
    for line in lines:
        x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
        y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
        line_row_i = y_1 // a4_guides_row_h
        if line_row_i > end_row_i - 1: 
            block_i += 1
            if block_i < len(blocks_list):
                start_col_i = blocks_list[block_i][0]
                start_row_i = blocks_list[block_i][1]
                end_row_i = blocks_list[block_i][2]
                line_i = 0
                x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
                y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
            else:
                break
                
        draw.text((x_1, y_1), line, (0, 0, 0), font=body_font)
        line_i += 1




def draw_body_justify(draw, lines, blocks_list):
    block_i = 0
    start_col_i = blocks_list[block_i][0]
    start_row_i = blocks_list[block_i][1]
    end_row_i = blocks_list[block_i][2]
    line_i = 0
    lines_num = len(lines)
    for i, line in enumerate(lines):
        x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
        y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
        line_row_i = y_1 // a4_guides_row_h
        if line_row_i > end_row_i - 1: 
            block_i += 1
            if block_i < len(blocks_list):
                start_col_i = blocks_list[block_i][0]
                start_row_i = blocks_list[block_i][1]
                end_row_i = blocks_list[block_i][2]
                line_i = 0
                x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
                y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
            else:
                break

        if i != lines_num - 1:
            words = line.split(" ")
            words_length = sum(draw.textlength(w, font=body_font) for w in words)
            space_length = ((a4_guides_col_w - a4_guides_col_gap*2) - words_length) / (len(words) - 1)
            x = x_1
            for word in words:
                draw.text((x, y_1), word, font=body_font, fill="black")
                x += draw.textlength(word, font=body_font) + space_length
        else:
            draw.text((x_1, y_1), line, font=body_font, fill="black")

        line_i += 1



def a4_body_blocks():
    cols_i_list = []
    if guides_col_num == 1:
        cols_i_list = [2]
    elif guides_col_num == 2:
        cols_i_list = [2, 8]
    elif guides_col_num == 3:
        cols_i_list = [2, 6, 10]
    blocks_list = []
    block_curr = ['', '', '']
    for col_i in range(g.GRID_COL_NUM):
        if col_i in cols_i_list:
            for row_i in range(g.GRID_ROW_NUM):
                if grid_map[row_i][col_i] == 'b':
                    if block_curr[0] == '': block_curr[0] = col_i
                    if block_curr[1] == '': block_curr[1] = row_i
                elif grid_map[row_i][col_i] != 'b':
                    if block_curr != ['', '', '']:
                        if block_curr[2] == '': block_curr[2] = row_i
                        blocks_list.append(block_curr)
                        block_curr = ['', '', '']
            if block_curr != ['', '', '']:
                if block_curr[2] == '': block_curr[2] = row_i
                blocks_list.append(block_curr)
                block_curr = block_curr = ['', '', '']
    return blocks_list





def text_to_lines(text):
    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        _, _, line_curr_w, _ = body_font.getbbox(line_curr)
        _, _, word_w, _ = body_font.getbbox(word)
        if line_curr_w + word_w < a4_guides_col_w - a4_guides_col_gap*2:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr)
    return lines





