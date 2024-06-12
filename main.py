
import os
import csv
import json
import time
from PIL import Image, ImageDraw, ImageFont

import g
import util
import util_ai

page_x = g.WINDOW_WIDTH//2-g.PAGE_WIDTH//2
page_y = g.WINDOW_HEIGHT//2-g.PAGE_HEIGHT//2

body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.BODY_FONT_SIZE)




####################################################################################################
# FUNC
####################################################################################################
def a4_draw_image(img, image_url):
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
    if col_i_x_1 != '' and col_i_y_1 != '' and col_i_x_2 != '' and col_i_y_2 != '':
        x_1 = int(a4_grid_col_w * col_i_x_1)
        y_1 = int(a4_grid_row_h * col_i_y_1)
        x_2 = int(a4_grid_col_w * (col_i_x_2 + 1))
        y_2 = int(a4_grid_row_h * (col_i_y_2 + 1))
        foreground = Image.open(image_url)
        fg_w = x_2 - x_1
        fg_h = y_2 - y_1
        foreground = util.img_resize(foreground, fg_w, fg_h)
        img.paste(foreground, (x_1, y_1))


def a4_draw_title(draw):
    title = 'Nature\'s \nWonderland'
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


def a4_draw_title_constrain(draw):
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
            lines.append(line_curr.strip())
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




####################################################################################################
# EXE
####################################################################################################
magazine_vol = '2024_06'
magazine_folderpath = f'database/{magazine_vol}'
magazine_pages_foldernames = os.listdir(magazine_folderpath)
for magazine_page_foldername in magazine_pages_foldernames:
    magazine_page_folderpath = f'{magazine_folderpath}/{magazine_page_foldername}'
    print(magazine_page_folderpath)

    # data
    json_filepath = f'{magazine_page_folderpath}/data.json'
    with open(json_filepath, 'r', encoding='utf-8') as f: 
        data = json.load(f)


    template_url = data['template_url']
    image_url = data['image_url']

    study_journal = data['study_journal']
    study_abstract = data['study_abstract']
    if 'body':
        key = 'body'
        # if key in data: del data[key]
        if key not in data:
            prompt = f'''
                Scrivi in Italiano un articolo di 400 parole per una rivista scientifica di ozono utilizzando i dati del seguente studio: {study_abstract}
                Inizia la risposta con queste parole: Secondo uno studio scientifico pubblicato dal {study_journal}, 
            '''
            reply = util_ai.gen_reply(prompt).strip()
            if reply != '':
                print('*********************************************************')
                print(reply)
                print('*********************************************************')
                data[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.SLEEP_TIME)
        if key in data:
            body = data['body'].replace('\n', ' ')

    # template
    with open(template_url, 'r', encoding='utf-8') as f: 
        data_template = json.load(f)
        
    grid_map = data_template['grid_map']

    # layout
    grid_col_num = 16 
    a4_grid_col_w = g.A4_WIDTH / grid_col_num

    grid_row_num = 16 
    a4_grid_row_h = g.A4_HEIGHT / grid_row_num

    guides_col_num = data_template['col_num']
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


    # magazine
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    a4_draw_image(img, image_url)
    a4_draw_title_constrain(draw)

    blocks_list = a4_body_blocks()

    if blocks_list != []:
        text = body
        lines = text_to_lines(text)
        draw_body_justify(draw, lines, blocks_list)

    export_url = data['export_url']
    img.save(export_url)
