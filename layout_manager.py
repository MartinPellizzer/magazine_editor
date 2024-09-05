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

# FLAGS
flag_brush_type = 't'
flag_window_grid = 1
flag_a4_grid = 1
flag_image_num = 1

flag_drag = False
drag_x_1 = -1
drag_y_1 = -1


# FONTS
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.BODY_FONT_SIZE)

# PAGE
page_x = g.WINDOW_WIDTH//2 - g.PAGE_WIDTH//2
page_y = g.WINDOW_HEIGHT//2 - g.PAGE_HEIGHT//2

# GRID
guide_sizes = [62, 71, 83, 99, 124, 165, 248]
guide_size_index = 0
guide_size = guide_sizes[guide_size_index]

grid_map = []
for row_i in range(g.GRID_ROW_NUM):
    row_curr = []
    for col_i in range(g.GRID_COL_NUM):
        row_curr.append('')
    grid_map.append(row_curr)

# MOUSE
mouse_click_col_i = 0
mouse_click_row_i = 0

# DATE
yyyy = '2024'
mm = '06'
month_folder = f'{yyyy}_{mm}'





####################################################################################################
# A4
####################################################################################################

def a4_draw_images(img):
    for i in range(10):
        col_i_x_1 = ''
        col_i_y_1 = ''
        col_i_x_2 = ''
        col_i_y_2 = ''
        is_first_pos = True
        for row_i in range(g.GRID_ROW_NUM):
            for col_i in range(g.GRID_COL_NUM):
                if f'i_{i}' in grid_map[row_i][col_i]:
                    if is_first_pos: 
                        col_i_x_1 = col_i
                        col_i_y_1 = row_i
                        is_first_pos = False
                    else:
                        col_i_x_2 = col_i
                        col_i_y_2 = row_i

        if col_i_x_1 != '' and col_i_y_1 != '' and col_i_x_2 != '' and col_i_y_2 != '':
            x_1 = g.A4_CELL_SIZE * col_i_x_1
            y_1 = g.A4_CELL_SIZE * col_i_y_1
            x_2 = g.A4_CELL_SIZE * (col_i_x_2 + 1)
            y_2 = g.A4_CELL_SIZE * (col_i_y_2 + 1)
            foreground = Image.open(f"assets/images/{i}.jpg")
            fg_w = x_2 - x_1
            fg_h = y_2 - y_1
            foreground = util.img_resize(foreground, fg_w, fg_h)
            img.paste(foreground, (x_1, y_1))




def a4_draw_text(draw):
    text = g.PLACEHOLDER_TEXT.replace('\n', '').strip()

    done_grid_map = []
    for row_i in range(g.GRID_ROW_NUM):
        row_curr = []
        for col_i in range(g.GRID_COL_NUM):
            row_curr.append('')
        done_grid_map.append(row_curr)
        
    lines_coord = []
    for col_i in range(g.GRID_COL_NUM):
        for row_i in range(g.GRID_ROW_NUM):
            if 'b' in grid_map[row_i][col_i]:
                if done_grid_map[row_i][col_i] != 'b':
                    done_grid_map[row_i][col_i] = 'b'
                    tmp_line_coord = []
                    for next_col_i in range(col_i, g.GRID_COL_NUM):
                        if 'b' in grid_map[row_i][next_col_i]:
                            done_grid_map[row_i][next_col_i] = 'b'
                            tmp_line_coord = [row_i, col_i, row_i, next_col_i+1]
                        else:
                            lines_coord.append(tmp_line_coord)
                            break

    for line_coord in lines_coord:
        words = text.split(' ')
        lines = []
        line_curr = ''
        for word in words:
            _, _, line_curr_w, _ = body_font.getbbox(line_curr)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_curr_w + word_w < (line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE:
                line_curr += f'{word} '
            else:
                lines.append(line_curr.strip())
                line_curr = f'{word} '
            if len(lines) >= 2: break
        lines.append(line_curr.strip())

        x_1 = g.A4_CELL_SIZE * line_coord[1]
        y_1 = g.A4_CELL_SIZE * line_coord[0]

        c_body = '#000000'
        if 'd' in grid_map[line_coord[0]][line_coord[1]]: c_body = '#ffffff'

        is_last_line = False
        for i, line in enumerate(lines):
            if i >= 2: break

            if len(lines) - i == 1:
                is_last_line = True
                print('last line')

            text = text.replace(line, '').strip()
            if not is_last_line:
                words = line.split(" ")
                print(len(lines), '>>', len(words))
                words_length = sum(draw.textlength(w, font=body_font) for w in words)
                space_length = (((line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE) - words_length) / (len(words) - 1)
                x = x_1
                for word in words:
                    draw.text((x, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), word, font=body_font, fill=c_body)
                    x += draw.textlength(word, font=body_font) + space_length
            else:
                draw.text((x_1, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), line, c_body, font=body_font)
                break

        if is_last_line: break


def a4_template_preview():
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    if flag_a4_grid:
        mag.a4_draw_grid(draw)
        mag.a4_draw_guides(draw, guide_size)

    a4_draw_images(img)
    mag.a4_draw_dark(draw, grid_map)
    mag.a4_draw_title(draw, grid_map, title='Nature\'s\nWonderland')
    a4_draw_text(draw)

    img.show()


def a4_template_save():
    templates_folderpath = f'templates'
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

    # save csv
    with open(f'templates/{last_template_id_str}.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(grid_map)

    # save image    
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    if flag_a4_grid:
        mag.a4_draw_grid(draw)
        mag.a4_draw_guides(draw, guide_size)
    a4_draw_images(img)
    mag.a4_draw_dark(draw, grid_map)
    mag.a4_draw_title(draw, grid_map, title='Nature\'s\nWonderland')
    a4_draw_text(draw)
    export_filepath = f'templates/{last_template_id_str}.jpg'
    img.save(export_filepath)
    




####################################################################################################
# WINDOW
####################################################################################################

def grid_map_copy():
    tmp = []
    for row_i in range(g.GRID_ROW_NUM):
        row_curr = []
        for col_i in range(g.GRID_COL_NUM):
            row_curr.append(grid_map[row_i][col_i])
        tmp.append(row_curr)
    return tmp





####################################################################################################
# PYGAME
####################################################################################################
pygame.init()

pygame.display.set_caption("Magazine Editor")
screen = pygame.display.set_mode((g.WINDOW_WIDTH, g.WINDOW_HEIGHT), 0, 32)
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 30)

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

            drag_c_1 = int((drag_x_1 - page_x) // g.GRID_CELL_SIZE)
            drag_r_1 = int((drag_y_1 - page_y) // g.GRID_CELL_SIZE)
            drag_c_2 = int((drag_x_2 - page_x) // g.GRID_CELL_SIZE)
            drag_r_2 = int((drag_y_2 - page_y) // g.GRID_CELL_SIZE)

            for row_i in range(g.GRID_ROW_NUM):
                for col_i in range(g.GRID_COL_NUM):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):

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
                                tmp_grid_map[row_i][col_i] += f'i_7'
                        if flag_brush_type == 'i' and flag_image_num == 8:
                            if 'i_8' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_8'
                        if flag_brush_type == 'i' and flag_image_num == 9:
                            if 'i_9' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_9'

                        if flag_brush_type == 'd':
                            if 'd' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 'd'
                        if flag_brush_type == 'b':
                            if 'b' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 'b'
                        if flag_brush_type == 't':
                            if 't' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 't'
        
        # clear blocks
        if pygame.mouse.get_pressed()[2]:
            tmp_grid_map = grid_map_copy()

            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - page_x) // g.GRID_CELL_SIZE)
            drag_r_1 = int((drag_y_1 - page_y) // g.GRID_CELL_SIZE)
            drag_c_2 = int((drag_x_2 - page_x) // g.GRID_CELL_SIZE)
            drag_r_2 = int((drag_y_2 - page_y) // g.GRID_CELL_SIZE)

            for row_i in range(g.GRID_ROW_NUM):
                for col_i in range(g.GRID_COL_NUM):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):

                        tmp_grid_map[row_i][col_i] = ''

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_0: flag_image_num = 0
            if event.key == pygame.K_1: flag_image_num = 1
            if event.key == pygame.K_2: flag_image_num = 2
            if event.key == pygame.K_3: flag_image_num = 3
            if event.key == pygame.K_4: flag_image_num = 4
            if event.key == pygame.K_5: flag_image_num = 5
            if event.key == pygame.K_6: flag_image_num = 6
            if event.key == pygame.K_7: flag_image_num = 7
            if event.key == pygame.K_8: flag_image_num = 8
            if event.key == pygame.K_9: flag_image_num = 9
            
            # if event.key == pygame.K_d: flag_brush_type = 'd'

            if event.key == pygame.K_SPACE:
                if flag_brush_type == 'i': flag_brush_type = 't'
                elif flag_brush_type == 't': flag_brush_type = 'b'
                elif flag_brush_type == 'b': flag_brush_type = 'd'
                elif flag_brush_type == 'd': flag_brush_type = 'i'
                
            if event.key == pygame.K_p:
                a4_template_preview()
                
            if event.key == pygame.K_g:
                flag_window_grid = not flag_window_grid
                
            # CTRL + S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                a4_template_save()
            
            if event.unicode == "+":
                if guide_size_index > 0: 
                    guide_size_index -= 1
                    guide_size = guide_sizes[guide_size_index]
            if event.unicode == "-":
                if guide_size_index < len(guide_sizes)-1: 
                    guide_size_index += 1
                    guide_size = guide_sizes[guide_size_index]
                
    # draw window bg
    pygame.draw.rect(screen, '#000000', (0, 0, g.PAGE_WIDTH, g.PAGE_HEIGHT))

    # draw page bg
    pygame.draw.rect(screen, '#ffffff', (page_x, page_y, g.PAGE_WIDTH, g.PAGE_HEIGHT))


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
    col_i = int((x_1 - page_x) // g.GRID_CELL_SIZE)
    row_i = int((y_1 - page_y) // g.GRID_CELL_SIZE)
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

    
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
            
            if 'i_1' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[0], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_2' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[1], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_3' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[2], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_4' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[3], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_5' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[4], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_6' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[5], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_7' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[6], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_8' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[7], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            if 'i_9' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, g.C_IMAGES[8], (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))

            if 'd' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, '#333333', (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))

            if 'b' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, '#000000', (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))
            
            if 't' in tmp_grid_map[row_i][col_i]:
                red_x_1 = page_x + g.GRID_CELL_SIZE * col_i
                red_y_1 = page_y + g.GRID_CELL_SIZE * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, g.GRID_CELL_SIZE, g.GRID_CELL_SIZE))


    if flag_window_grid:
        i = 0
        for _ in range(9999):
            if g.GRID_CELL_SIZE * i > g.PAGE_WIDTH: break
            x_1 = page_x + g.GRID_CELL_SIZE * i
            y_1 = page_y
            x_2 = page_x + g.GRID_CELL_SIZE * i
            y_2 = page_y + g.PAGE_HEIGHT
            pygame.draw.line(screen, g.C_GRID, (int(x_1), y_1), (int(x_2), y_2), 2)
            i += 1  
        i = 0
        for _ in range(9999):
            if g.GRID_CELL_SIZE * i > g.PAGE_HEIGHT: break
            x_1 = page_x
            y_1 = page_y + g.GRID_CELL_SIZE * i
            x_2 = page_x + g.PAGE_WIDTH
            y_2 = page_y + g.GRID_CELL_SIZE * i
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

        i = 0
        for _ in range(9999):
            if guide_size * i > g.PAGE_HEIGHT: break
            x_1 = page_x
            y_1 = page_y + guide_size * i
            x_2 = page_x + g.PAGE_WIDTH
            y_2 = page_y + guide_size * i
            pygame.draw.line(screen, g.C_GUIDE, (int(x_1), y_1), (int(x_2), y_2), 2)
            i += 1

    pygame.display.update()
