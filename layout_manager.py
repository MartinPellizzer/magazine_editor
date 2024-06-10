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





screen = pygame.display.set_mode((window_w, window_h), 0, 32)

pygame.display.set_caption("Magazine Editor")

background = pygame.image.load(background_image).convert()
mouse_cursor = pygame.image.load(mouse_image).convert()
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 30)



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

    

def preview_page():
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


    # draw title
    title = 'Nature\'s \nWonderland'
    title_font_size = 200
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
    title_col_i = ''
    title_row_i = ''
    for row_i in range(a4_grid_row_num):
        for col_i in range(a4_grid_col_num):
            if grid_map[row_i][col_i] == 't':
                title_col_i = col_i
                title_row_i = row_i
                break
    
    if title_col_i != '' and title_row_i != '':
        x_1 = a4_grid_col_w * title_col_i
        y_1 = a4_grid_row_h * title_row_i
        draw.text((x_1, y_1), title, (0, 0, 0), font=title_font)


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

    # draw body
    with open('demo_article.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
    text = text.replace('\n', ' ')

    blocks_list = []
    block_curr = ['', '', '']
    for col_i in range(a4_grid_col_num):
        if col_i == 2 or col_i == 6 or col_i == 10:
            for row_i in range(a4_grid_row_num):
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



def template_save():
    templates_filenames = os.listdir('templates')
    last_template_id = 0
    for template_filename in templates_filenames:
        last_template_id = int(template_filename.split('.')[0])
    last_template_id += 1

    last_template_id_str = ''
    if last_template_id < 10: last_template_id_str = f'000{last_template_id}'
    elif last_template_id < 100: last_template_id_str = f'00{last_template_id}'
    elif last_template_id < 1000: last_template_id_str = f'0{last_template_id}'
    elif last_template_id < 10000: last_template_id_str = f'{last_template_id}'
    print(last_template_id_str)

    with open(f'templates/{last_template_id_str}.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(grid_map)



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
            print(grid_map)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('key left')
            if event.key == pygame.K_RIGHT:
                print('key right')

            # CTRL + G
            if event.key == pygame.K_g and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                flag_a4_grid = not flag_a4_grid
            # G
            elif event.key == pygame.K_g:
                show_grid = not show_grid

            # CTRL + S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                template_save()

            # PREVIEW
            if event.key == pygame.K_p:
                preview_page()
            
            # BRUSH
            if event.key == pygame.K_SPACE:
                if flag_brush_type == 't': flag_brush_type = 'b'
                elif flag_brush_type == 'b': flag_brush_type = 'i'
                elif flag_brush_type == 'i': flag_brush_type = 't'
            

    # draw_background()
    pygame.draw.rect(screen, '#000000', (0, 0, page_w, page_h))

    # draw_page()
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, page_w, page_h))


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