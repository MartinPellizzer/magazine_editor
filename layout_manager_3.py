import pygame
from pygame.locals import *
from sys import exit

import os
import csv
import json
from PIL import Image, ImageDraw, ImageFont
import random

import g
import util
import mag






####################################################################################################
# VAR
####################################################################################################


C_IMAGES = [
    '#41EAD4',
    '#FF9F1C',
    '#2A1E5C',
    '#55286F',
    '#8EA604',
    '#FF4E00',
    '#2AB7CA',
    '#717C89',
    '#ADF6B1',
    '#223127',
    '#CE5374',
]

# FLAGS
flag_a4_grid = 0
flag_brush_type = 'i'
show_grid = 1
flag_image_num = 0

# FONTS
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.BODY_FONT_SIZE)

# PAGE
page_x = g.WINDOW_WIDTH//2 - g.PAGE_WIDTH//2
page_y = g.WINDOW_HEIGHT//2 - g.PAGE_HEIGHT//2

# GRID
cell_size = 16
guide_size_8 = 62
guide_size_7 = 71
guide_size_6 = 83
guide_size_5 = 99
guide_size_4 = 124
guide_size_3 = 165
guide_size_2 = 248
guide_size = guide_size_6


grid_col_num = 16 
a4_grid_col_w = g.A4_WIDTH / grid_col_num

grid_row_num = 16 
a4_grid_row_h = g.A4_HEIGHT / grid_row_num

guides_col_num = 2
a4_guides_col_padding = a4_grid_col_w*4
a4_guides_col_gap = 16
a4_guides_col_w = (g.A4_WIDTH - a4_guides_col_padding) / guides_col_num

guides_row_num = 12
a4_guides_row_padding = a4_grid_row_h*4
a4_guides_row_h = (g.A4_HEIGHT - a4_guides_row_padding) / guides_row_num

page_grid_col_w = g.PAGE_WIDTH / grid_col_num
page_grid_row_h = g.PAGE_HEIGHT / grid_row_num

page_guides_col_padding = page_grid_col_w*4
page_guides_col_w = (g.PAGE_WIDTH - page_guides_col_padding) / guides_col_num

page_guides_row_padding = page_grid_row_h*4
page_guides_row_h = (g.PAGE_HEIGHT - page_guides_row_padding) / guides_row_num


grid_col_num = int(g.PAGE_WIDTH / cell_size)
grid_row_num = int(g.PAGE_HEIGHT / cell_size) + 1

grid_map = []
for row_i in range(grid_row_num):
    row_curr = []
    for col_i in range(grid_col_num):
        row_curr.append('')
    grid_map.append(row_curr)


for row_i in range(grid_row_num):
    for col_i in range(grid_col_num):
        if (col_i > 4 and col_i < 12 and 
            row_i > 8 and row_i < 24): 
            grid_map[row_i][col_i] = 'b'
        if (col_i > 14 and col_i < 18 and 
            row_i > 8 and row_i < 16): 
            grid_map[row_i][col_i] = 'b'

# MOUSE
mouse_click_col_i = 0
mouse_click_row_i = 0

# DATE
yyyy = '2024'
mm = '06'
month_folder = f'{yyyy}_{mm}'





####################################################################################################
# FUNC
####################################################################################################

def a4_draw_grid_2(draw):
    for i in range(grid_col_num+1):
        x_1 = int(cell_size*10/2*i)
        y_1 = 0
        x_2 = int(cell_size*10/2*i)
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)
    for i in range(grid_row_num+1):
        x_1 = 0
        y_1 = int(cell_size*10/2*i)
        x_2 = g.A4_WIDTH
        y_2 = int(cell_size*10/2*i)
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)


def a4_draw_guides_2(draw):
    for i in range(grid_col_num+1):
        x_1 = int(guide_size*10/2*i)
        y_1 = 0
        x_2 = int(guide_size*10/2*i)
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GUIDE, width=8)



def a4_draw_title(draw):
    title = 'Nature\'s Wonderland'
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.TITLE_FONT_SIZE)
    title_col_i = ''
    title_row_i = ''
    for row_i in range(grid_row_num):
        for col_i in range(grid_col_num):
            if grid_map[row_i][col_i] == 't':
                title_col_i = col_i
                title_row_i = row_i
                break
    if title_col_i != '' and title_row_i != '':
        x_1 = a4_grid_col_w * title_col_i
        y_1 = a4_grid_row_h * title_row_i
        draw.text((x_1, y_1), title, (0, 0, 0), font=title_font)


def a4_draw_title_2(draw):
    title = 'Nature\'s Wonderland'
    title = 'This is a title'
    title = 'How to sanitize poultry\nmeat with ozone'
    # title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.TITLE_FONT_SIZE)

    col_i_1 = -1
    row_i_1 = -1
    col_i_2 = -1
    row_i_2 = -1
    for row_i in range(grid_row_num):
        for col_i in range(grid_col_num):
            if grid_map[row_i][col_i] == 't':
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i

    # print(col_i_1, row_i_1)
    # print(col_i_2, row_i_2)

    title_available_w = (col_i_2 - col_i_1 + 1) * a4_grid_col_w
    title_available_h = (row_i_2 - row_i_1 + 1) * a4_grid_row_h
    # print(title_available_w)

    lines = title.split('\n')
    line_longest = ''
    for line in lines:
        if len(line_longest) < len(line): line_longest = line
    
    title_font_size = 1
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
    for _ in range(999):
        title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
        _, _, title_curr_w, title_curr_h = title_font.getbbox(line_longest)
        if title_curr_w > title_available_w or title_curr_h > title_available_h:
            break
        else:
            title_font_size += 1




    if col_i_1 != -1 and row_i_1 != -1 and col_i_2 != -1 and row_i_2 != -1:
        x_1 = a4_grid_col_w * col_i_1
        y_1 = a4_grid_row_h * row_i_1
        draw.text((x_1, y_1), title, (0, 0, 0), font=title_font)


def a4_draw_image_2(img):
    col_i_x_1 = ''
    col_i_y_1 = ''
    col_i_x_2 = ''
    col_i_y_2 = ''
    is_first_pos = True
    for row_i in range(grid_row_num):
        for col_i in range(grid_col_num):
            if grid_map[row_i][col_i] == 'i':
                if is_first_pos: 
                    col_i_x_1 = col_i
                    col_i_y_1 = row_i
                    is_first_pos = False
                else:
                    col_i_x_2 = col_i
                    col_i_y_2 = row_i

    print(col_i_x_1, col_i_y_1, col_i_x_2, col_i_y_2)
    if col_i_x_1 != '' and col_i_y_1 != '' and col_i_x_2 != '' and col_i_y_2 != '':
        x_1 = int(cell_size*10/2 * col_i_x_1)
        y_1 = int(cell_size*10/2 * col_i_y_1)
        x_2 = int(cell_size*10/2 * (col_i_x_2 + 1))
        y_2 = int(cell_size*10/2 * (col_i_y_2 + 1))
        foreground = Image.open("picture.jpg")
        fg_w = x_2 - x_1
        fg_h = y_2 - y_1
        foreground = util.img_resize(foreground, fg_w, fg_h)
        img.paste(foreground, (x_1, y_1))


def a4_draw_image_3(img):
    for i in range(10):
        col_i_x_1 = ''
        col_i_y_1 = ''
        col_i_x_2 = ''
        col_i_y_2 = ''
        is_first_pos = True
        for row_i in range(grid_row_num):
            for col_i in range(grid_col_num):
                if f'i_{i}' in grid_map[row_i][col_i]:
                    if is_first_pos: 
                        col_i_x_1 = col_i
                        col_i_y_1 = row_i
                        is_first_pos = False
                    else:
                        col_i_x_2 = col_i
                        col_i_y_2 = row_i

        if col_i_x_1 != '' and col_i_y_1 != '' and col_i_x_2 != '' and col_i_y_2 != '':
            x_1 = int(cell_size*10/2 * col_i_x_1)
            y_1 = int(cell_size*10/2 * col_i_y_1)
            x_2 = int(cell_size*10/2 * (col_i_x_2 + 1))
            y_2 = int(cell_size*10/2 * (col_i_y_2 + 1))
            foreground = Image.open(f"assets/images/{i}.jpg")
            fg_w = x_2 - x_1
            fg_h = y_2 - y_1
            foreground = util.img_resize(foreground, fg_w, fg_h)
            img.paste(foreground, (x_1, y_1))


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
    for col_i in range(grid_col_num):
        if col_i in cols_i_list:
            for row_i in range(grid_row_num):
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
            lines.append(line_curr)
            line_curr = f'{word} '
    lines.append(line_curr)
    return lines


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





def template_preview_2():
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    if flag_a4_grid:
        a4_draw_grid_2(draw)
        a4_draw_guides_2(draw)

    a4_draw_image_3(img)

    
    done_grid_map = []
    for row_i in range(grid_row_num):
        row_curr = []
        for col_i in range(grid_col_num):
            row_curr.append('')
        done_grid_map.append(row_curr)
        
    # get body blocks (lines)
    lines_coord = []
    for col_i in range(grid_col_num):
        for row_i in range(grid_row_num):
            if grid_map[row_i][col_i] == 'b':
                if done_grid_map[row_i][col_i] != 'b':
                    done_grid_map[row_i][col_i] = 'b'
                    tmp_line_coord = []
                    for next_col_i in range(col_i, grid_col_num):
                        if grid_map[row_i][next_col_i] == 'b':
                            done_grid_map[row_i][next_col_i] = 'b'
                            tmp_line_coord = [row_i, col_i, row_i, next_col_i]
                        else:
                            lines_coord.append(tmp_line_coord)
                            break



    text = g.PLACEHOLDER_TEXT.replace('\n', '').strip()

    for line_coord in lines_coord:
        words = text.split(' ')
        lines = []
        line_curr = ''
        for word in words:
            _, _, line_curr_w, _ = body_font.getbbox(line_curr)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_curr_w + word_w < (line_coord[3] - line_coord[1]) * int(cell_size*10/2):
                line_curr += f'{word} '
            else:
                lines.append(line_curr.strip())
                line_curr = f'{word} '
        lines.append(line_curr.strip())

        x_1 = int(cell_size*10/2) * line_coord[1]
        y_1 = int(cell_size*10/2) * line_coord[0]
        for i, line in enumerate(lines):
            if i >= 2: break
            text = text.replace(line, '').strip()
            draw.text((x_1, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), line, (0, 0, 0), font=body_font)

    img.show()


def template_jpg_save(last_template_id_str):
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    if flag_a4_grid:
        a4_draw_grid_2(draw)
        a4_draw_guides(draw)

    a4_draw_title(draw)
    a4_draw_image_3(img)

    blocks_list = a4_body_blocks()

    if blocks_list != []:
        text = g.DEMO_TEXT
        lines = text_to_lines(text)
        draw_body(draw, lines, blocks_list)

    export_filepath = f'templates/{month_folder}/{last_template_id_str}.jpg'
    img.save(export_filepath)


def template_save():
    templates_folderpath = f'templates/{month_folder}'
    templates_filenames = os.listdir(templates_folderpath)
    last_template_id = 0
    for template_filename in templates_filenames:
        last_template_id = int(template_filename.split('.')[0])
    last_template_id += 1

    last_template_id_str = ''
    if last_template_id < 10: last_template_id_str = f'000{last_template_id}'
    elif last_template_id < 100: last_template_id_str = f'00{last_template_id}'
    elif last_template_id < 1000: last_template_id_str = f'0{last_template_id}'
    elif last_template_id < 10000: last_template_id_str = f'{last_template_id}'

    with open(f'templates/{month_folder}/{last_template_id_str}.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(grid_map)

    data = {}
    data['col_num'] = guides_col_num
    data['grid_map'] = grid_map
    with open(f'templates/{month_folder}/{last_template_id_str}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    template_jpg_save(last_template_id_str)
    




####################################################################################################
# PYGAME
####################################################################################################
pygame.init()

screen = pygame.display.set_mode((g.WINDOW_WIDTH, g.WINDOW_HEIGHT), 0, 32)

pygame.display.set_caption("Magazine Editor")
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 30)

flag_drag = False
drag_x_1 = -1
drag_y_1 = -1

tmp_grid_map = []

def grid_map_copy():
    tmp = []
    for row_i in range(grid_row_num):
        row_curr = []
        for col_i in range(grid_col_num):
            row_curr.append(grid_map[row_i][col_i])
        tmp.append(row_curr)
    return tmp

tmp_grid_map = grid_map_copy()

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag_drag = True
            pos = pygame.mouse.get_pos()
            drag_x_1 = pos[0]
            drag_y_1 = pos[1]
            print(flag_drag)

        if event.type == pygame.MOUSEBUTTONUP:
            flag_drag = False
            grid_map = tmp_grid_map

        # draw blocks
        if pygame.mouse.get_pressed()[0]:
            tmp_grid_map = grid_map_copy()

            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - page_x) // cell_size)
            drag_r_1 = int((drag_y_1 - page_y) // cell_size)
            drag_c_2 = int((drag_x_2 - page_x) // cell_size)
            drag_r_2 = int((drag_y_2 - page_y) // cell_size)

            for row_i in range(grid_row_num):
                for col_i in range(grid_col_num):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):

                        if flag_brush_type == 't':
                            tmp_grid_map[row_i][col_i] = 't'
                        if flag_brush_type == 'b':
                            tmp_grid_map[row_i][col_i] = 'b'
                        if flag_brush_type == 'i' and flag_image_num == 0:
                            if 'i_0' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_0'
                        if flag_brush_type == 'i' and flag_image_num == 1:
                            if 'i_1' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_1'
                        if flag_brush_type == 'i' and flag_image_num == 2:
                            if 'i_2' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_2'
                        if flag_brush_type == 'i' and flag_image_num == 3:
                            if 'i_3' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_3'
                        if flag_brush_type == 'i' and flag_image_num == 4:
                            if 'i_4' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_4'
                        if flag_brush_type == 'i' and flag_image_num == 5:
                            if 'i_5' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_5'
                        if flag_brush_type == 'i' and flag_image_num == 6:
                            if 'i_6' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_6'
                        if flag_brush_type == 'i' and flag_image_num == 7:
                            if 'i_7' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_8'
                        if flag_brush_type == 'i' and flag_image_num == 8:
                            if 'i_8' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_8'
                        if flag_brush_type == 'i' and flag_image_num == 9:
                            if 'i_9' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_9'
        
        # clear blocks
        if pygame.mouse.get_pressed()[2]:
            tmp_grid_map = grid_map_copy()

            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - page_x) // cell_size)
            drag_r_1 = int((drag_y_1 - page_y) // cell_size)
            drag_c_2 = int((drag_x_2 - page_x) // cell_size)
            drag_r_2 = int((drag_y_2 - page_y) // cell_size)

            for row_i in range(grid_row_num):
                for col_i in range(grid_col_num):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):

                        tmp_grid_map[row_i][col_i] = ''

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0: flag_image_num = 0
            if event.key == pygame.K_1: flag_image_num = 1
            if event.key == pygame.K_2: flag_image_num = 2
            if event.key == pygame.K_3: flag_image_num = 3
            if event.key == pygame.K_4: flag_image_num = 4
            if event.key == pygame.K_5: flag_image_num = 5
            if event.key == pygame.K_6: flag_image_num = 6
            if event.key == pygame.K_7: flag_image_num = 7
            if event.key == pygame.K_8: flag_image_num = 8
            if event.key == pygame.K_9: flag_image_num = 9

            if event.key == pygame.K_SPACE:
                if flag_brush_type == 't': flag_brush_type = 'b'
                elif flag_brush_type == 'b': flag_brush_type = 'i'
                elif flag_brush_type == 'i': flag_brush_type = 't'
                
            if event.key == pygame.K_p:
                template_preview_2()
                
            # CTRL + S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                template_save()
            
            if event.unicode == "+":
                if guide_size == guide_size_2: guide_size = guide_size_3
                elif guide_size == guide_size_3: guide_size = guide_size_4
                elif guide_size == guide_size_4: guide_size = guide_size_5
                elif guide_size == guide_size_5: guide_size = guide_size_6
                elif guide_size == guide_size_6: guide_size = guide_size_7
                elif guide_size == guide_size_7: guide_size = guide_size_8
                # guide_size += 1
                print(guide_size)
            if event.unicode == "-":
                if guide_size == guide_size_8: guide_size = guide_size_7
                elif guide_size == guide_size_7: guide_size = guide_size_6
                elif guide_size == guide_size_6: guide_size = guide_size_5
                elif guide_size == guide_size_5: guide_size = guide_size_4
                elif guide_size == guide_size_4: guide_size = guide_size_3
                elif guide_size == guide_size_3: guide_size = guide_size_2
                # guide_size -= 1
                print(guide_size)
                
    # draw window bg
    pygame.draw.rect(screen, '#000000', (0, 0, g.PAGE_WIDTH, g.PAGE_HEIGHT))

    # draw page bg
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, g.PAGE_WIDTH, g.PAGE_HEIGHT))


    i = 0
    for _ in range(9999):
        if cell_size * i > g.PAGE_WIDTH: break
        x_1 = page_x + cell_size * i
        y_1 = page_y
        x_2 = page_x + cell_size * i
        y_2 = page_y + g.PAGE_HEIGHT
        pygame.draw.line(screen, g.C_GRID, (int(x_1), y_1), (int(x_2), y_2), 2)
        i += 1  
    i = 0
    for _ in range(9999):
        if cell_size * i > g.PAGE_HEIGHT: break
        x_1 = page_x
        y_1 = page_y + cell_size * i
        x_2 = page_x + g.PAGE_WIDTH
        y_2 = page_y + cell_size * i
        pygame.draw.line(screen, g.C_GRID, (x_1, int(y_1)), (x_2, int(y_2)), 2)
        i += 1

    i = 0
    for _ in range(9999):
        if guide_size * i > g.PAGE_WIDTH: break
        x_1 = page_x + guide_size * i
        y_1 = page_y
        x_2 = page_x + guide_size * i
        y_2 = page_y + g.PAGE_HEIGHT
        pygame.draw.line(screen, g.C_GUIDE, (int(x_1), y_1), (int(x_2), y_2), 2)
        i += 1

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
    col_i = int((x_1 - page_x) // cell_size)
    row_i = int((y_1 - page_y) // cell_size)
    text_surface = my_font.render(f'{col_i}:{row_i}', False, '#ff00ff')
    screen.blit(text_surface, (0, 60))
    
    # flags
    text_surface = my_font.render(f'flag_a4_grid:{flag_a4_grid}', False, '#ff00ff')
    screen.blit(text_surface, (0, 120))
    text_surface = my_font.render(f'flag_brush_type:{flag_brush_type}', False, '#ff00ff')
    screen.blit(text_surface, (0, 150))
    text_surface = my_font.render(f'div:{g.PAGE_WIDTH/guide_size}', False, '#ff00ff')
    screen.blit(text_surface, (0, 180))
    text_surface = my_font.render(f'div:{g.PAGE_HEIGHT/guide_size}', False, '#ff00ff')
    screen.blit(text_surface, (0, 210))

    # img num
    text_surface = my_font.render(f'image_num:{flag_image_num}', False, '#ff00ff')
    screen.blit(text_surface, (0, 240))

    
    for row_i in range(grid_row_num):
        for col_i in range(grid_col_num):
            if tmp_grid_map[row_i][col_i] == 't':
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, cell_size, cell_size))
            if tmp_grid_map[row_i][col_i] == 'b':
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, '#000000', (red_x_1, red_y_1, cell_size, cell_size))

            if 'i_0' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[0], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_1' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[1], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_2' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[2], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_3' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[3], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_4' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[4], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_5' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[5], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_6' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[6], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_7' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[7], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_8' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[8], (red_x_1, red_y_1, cell_size, cell_size))
            if 'i_9' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + cell_size * col_i
                red_y_1 = page_y + cell_size * row_i
                pygame.draw.rect(screen, C_IMAGES[9], (red_x_1, red_y_1, cell_size, cell_size))

    pygame.display.update()