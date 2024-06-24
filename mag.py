import os
from PIL import Image, ImageDraw, ImageFont

import g
import util


def a4_draw_grid(draw):
    for i in range(g.GRID_COL_NUM+1):
        x_1 = g.A4_CELL_SIZE*i
        y_1 = 0
        x_2 = g.A4_CELL_SIZE*i
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)

    for i in range(g.GRID_ROW_NUM+1):
        x_1 = 0
        y_1 = g.A4_CELL_SIZE*i
        x_2 = g.A4_WIDTH
        y_2 = g.A4_CELL_SIZE*i
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)


def a4_draw_guides(draw, guide_size):
    for i in range(g.GRID_COL_NUM+1):
        x_1 = int(guide_size*10/2*i)
        y_1 = 0
        x_2 = int(guide_size*10/2*i)
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GUIDE, width=8)


def a4_draw_images(img, img_folder, grid_map):
    img_filapaths = [f'{img_folder}/{filename}' for filename in os.listdir(img_folder) if filename.endswith('.jpg')]
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

            foreground = Image.open(img_filapaths[i])

            fg_w = x_2 - x_1
            fg_h = y_2 - y_1
            foreground = util.img_resize(foreground, fg_w, fg_h)
            img.paste(foreground, (x_1, y_1))


def a4_draw_dark(draw, grid_map):
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
            if 'd' in grid_map[row_i][col_i]:
                x_1 = g.A4_CELL_SIZE * col_i
                y_1 = g.A4_CELL_SIZE * row_i
                x_2 = x_1 + g.A4_CELL_SIZE
                y_2 = y_1 + g.A4_CELL_SIZE
                draw.rectangle(
                    (
                        (x_1, y_1), 
                        (x_2, y_2)
                    ), 
                    fill="#020617"
                )




def a4_draw_title(draw, grid_map, title):
    col_i_1 = -1
    row_i_1 = -1
    col_i_2 = -1
    row_i_2 = -1
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
            if 't' in grid_map[row_i][col_i]:
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i

    title_available_w = (col_i_2 - col_i_1 + 1) * g.A4_CELL_SIZE
    title_available_h = (row_i_2 - row_i_1 + 1) * g.A4_CELL_SIZE

    # title = 'This is a title'
    # title = 'How to sanitize poultry\nmeat with ozone'

    lines = title.split('\n')
    line_longest = ''
    for line in lines:
        if len(line_longest) < len(line): line_longest = line

    text_color = '#000000'
    if 'd' in grid_map[row_i_1][col_i_1]: text_color = '#ffffff'
    
    title_font_size = 1
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
    for _ in range(999):
        # print(title_font_size)
        title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
        _, _, title_curr_w, title_curr_h = title_font.getbbox(line_longest)
        if title_curr_w > title_available_w or title_curr_h > title_available_h:
            break
        else:
            title_font_size += 1

    if col_i_1 != -1 and row_i_1 != -1 and col_i_2 != -1 and row_i_2 != -1:
        x_1 = g.A4_CELL_SIZE * col_i_1
        y_1 = g.A4_CELL_SIZE * row_i_1
        draw.text((x_1, y_1), title, text_color, font=title_font)


def a4_draw_title_new(draw, grid_map, title):
    col_i_1 = -1
    row_i_1 = -1
    col_i_2 = -1
    row_i_2 = -1
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
            if 't' in grid_map[row_i][col_i]:
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i

    title_available_w = (col_i_2 - col_i_1 + 1) * g.A4_CELL_SIZE
    title_available_h = (row_i_2 - row_i_1 + 1) * g.A4_CELL_SIZE

    # title = 'This is a title'
    # title = 'How to sanitize poultry\nmeat with ozone'

    lines = title.split('\n')
    line_longest = ''
    for line in lines:
        if len(line_longest) < len(line): line_longest = line

    text_color = '#000000'
    if 'd' in grid_map[row_i_1][col_i_1]: text_color = '#ffffff'
    
    title_font_size = 1
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
    for _ in range(999):
        # print(title_font_size)
        title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", title_font_size)
        _, _, title_curr_w, title_curr_h = title_font.getbbox(line_longest)
        if title_curr_w > title_available_w or title_curr_h > title_available_h:
            break
        else:
            title_font_size += 1

    if col_i_1 != -1 and row_i_1 != -1 and col_i_2 != -1 and row_i_2 != -1:
        x_1 = g.A4_CELL_SIZE * col_i_1
        y_1 = g.A4_CELL_SIZE * row_i_1
        draw.text((x_1, y_1), title, text_color, font=title_font)


def a4_draw_text_study(draw, text, grid_map, commit):
    text_total = text
    text_words_written = 0
    body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.BODY_FONT_SIZE)

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

    line_coord_index = 0
    line_coord = lines_coord[line_coord_index]
    x_start = g.A4_CELL_SIZE * line_coord[1]
    y_start = g.A4_CELL_SIZE * line_coord[0]

    
    x_1 = x_start
    y_1 = y_start
    for i in range(999):
        if line_coord_index >= len(lines_coord) - 1: break
        cell_row_i = y_1 // g.A4_CELL_SIZE
        cell_col_i = x_1 // g.A4_CELL_SIZE
        if cell_row_i != line_coord[0]:
            line_coord_index += 1
            line_coord = lines_coord[line_coord_index]
            if cell_row_i != line_coord[0]:
                x_1 = g.A4_CELL_SIZE * line_coord[1]
                y_1 = g.A4_CELL_SIZE * line_coord[0]

        words = text.split(' ')
        line = ''
        is_last_line = True
        is_break_line = False
        for word in words:
            if word == '<break>':
                line = ''
                is_last_line = False
                is_break_line = True
                break
            _, _, line_w, _ = body_font.getbbox(line)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_w + word_w < (line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE:
                line += f'{word} '
            else:
                line = line.strip()
                is_last_line = False
                break

        is_paragraph_last_line = False
        if '\n' in line:
            line = line.split('\n')[0]
            is_paragraph_last_line = True

        c_body = '#000000'
        if 'd' in grid_map[line_coord[0]][line_coord[1]]: c_body = '#ffffff'

        text_words_written += len(line.split(' '))

        if not is_last_line:
            if not is_paragraph_last_line:
                words = line.split(" ")
                words_length = sum(draw.textlength(w, font=body_font) for w in words)
                if len(words) != 1:
                    space_length = (((line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE) - words_length) / (len(words) - 1)
                else:
                    space_length = (((line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE) - words_length) / (len(words))
                x = x_1
                for word in words:
                    if commit: draw.text((x, y_1), word, font=body_font, fill=c_body)
                    x += draw.textlength(word, font=body_font) + space_length
            else:
                if commit: draw.text((x_1, y_1), line, c_body, font=body_font)
        else:
            if commit: draw.text((x_1, y_1), line, c_body, font=body_font)
            is_last_line = True
            break

        y_1 += g.BODY_FONT_SIZE * 1.3
        text = text.replace(line, '', 1).strip()

        if is_paragraph_last_line:
            text = '<break> ' + text
        
        if is_break_line:
            text = text.replace('<break>', '', 1).strip()

    text_words_total = len(text_total.split(' '))
    print(f'text words total: {text_words_total}')
    print(f'text words written: {text_words_written}')
    
    return is_last_line
