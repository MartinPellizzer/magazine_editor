import os
from PIL import Image, ImageDraw, ImageFont

import g
import util

font_text = 'assets/fonts/Lato/Lato-Regular.ttf'

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
    title_font = ImageFont.truetype(font_text, title_font_size)
    for _ in range(999):
        # print(title_font_size)
        title_font = ImageFont.truetype(font_text, title_font_size)
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
    # GET TITLE BOX
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

    # GET TITLE MAX WIDTH AND HEIGHT
    title_available_w = (col_i_2 - col_i_1 + 1) * g.A4_CELL_SIZE
    title_available_h = (row_i_2 - row_i_1) * g.A4_CELL_SIZE

    # SPLIT TITLE BY "N"
    for lines_num in range(1, 9):
        title_words_num = len(title.split(' ')) 
        line_words_num = title_words_num // lines_num

        words = title.split(' ')
        lines = []
        line_curr = ''
        i = 0
        for word in words:
            if i < line_words_num:
                line_curr += f'{word} '
                i += 1
            else:
                lines.append(line_curr)
                line_curr = f'{word} '
                i = 0
        lines.append(line_curr)
            
        # GET TITLE LINE MAX WIDTH
        line_longest = ''
        for line in lines:
            if len(line_longest) < len(line): line_longest = line
        
        lines = '\n'.join(lines)

        # CHOOSE TITLE COLOR
        text_color = '#000000'
        if 'd' in grid_map[row_i_1][col_i_1]: text_color = '#ffffff'
        
        # CALC TITLE SIZE
        title_font_size = 1
        title_font = ImageFont.truetype(font_text, title_font_size)
        for _ in range(999):
            title_font = ImageFont.truetype(font_text, title_font_size)
            _, _, title_curr_w, title_curr_h = title_font.getbbox(line_longest)
            if title_curr_w > title_available_w or title_curr_h > title_available_h:
                break
            else:
                title_font_size += 1

        lines_h = title_font_size * lines_num
        # for line in lines.split('\n'):
        #     _, _, _, line_h = title_font.getbbox(line)
        #     lines_h += line_h
        print(lines_h , title_available_h)
        if lines_h > title_available_h: break

    # DRAW TITLE
    if col_i_1 != -1 and row_i_1 != -1 and col_i_2 != -1 and row_i_2 != -1:
        x_1 = g.A4_CELL_SIZE * col_i_1
        y_1 = g.A4_CELL_SIZE * row_i_1
        draw.text((x_1, y_1), lines, text_color, font=title_font)


def a4_draw_title_constrained_y(draw, grid_map, title):
    # GET TITLE BOX
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

    print(row_i_1, col_i_1, row_i_2, col_i_2)

    

    # title = ['this is a', 'test title']
    # lines = title
    
    # title_words = title.split(' ')
    # title_words_num = len(title_words)
    # lines_num = 4
    # line_words_num = title_words_num // lines_num
    # lines = []
    # line = []
    # for i, word in enumerate(title_words):
    #     if len(line) < line_words_num:
    #         line.append(word)
    #     else:
    #         line.append(word)
    #         lines.append(' '.join(line))
    #         line = []
    # lines.append(' '.join(line))

    x_1 = g.A4_CELL_SIZE * col_i_1
    y_1 = g.A4_CELL_SIZE * row_i_1
    x_2 = g.A4_CELL_SIZE * (col_i_2 + 1)
    y_2 = g.A4_CELL_SIZE * (row_i_2 + 1)
    
    # draw.rectangle(
    #     (
    #         (x_1, y_1), 
    #         (x_2, y_2)
    #     ), 
    #     fill="#ff0000"
    # )

    title_available_w = x_2 - x_1
    title_available_h = y_2 - y_1

    title_color = '#000000'
    if 'd' in grid_map[row_i_1][col_i_1]: title_color = '#ffffff'

    print(title)
    title_words_num = len(title.split(' '))
    line_1 = ' '.join(title.split(' ')[0:title_words_num-4])
    line_2 = ' '.join(title.split(' ')[title_words_num-4:title_words_num-1])
    line_3 = ' '.join(title.split(' ')[title_words_num-1:])
    # lines = [title]
    lines = [line_1, line_2, line_3]
    print(lines)
    # quit()

    # lines_num = 1
    # i = 0
    # for _ in range(999):
    #     title_font_size = i
    #     title_font = ImageFont.truetype(font_text, title_font_size)

    #     # get lines sizes
    #     lines_height_total = 0
    #     lines_width_max = 0
    #     lines_width_max_index = 0
    #     lines_height_max = 0
    #     for line_index, line in enumerate(lines):
    #         _, _, line_w, line_h = title_font.getbbox(line)
    #         lines_height_total += line_h
    #         if lines_width_max < line_w: 
    #             lines_width_max = line_w
    #             lines_width_max_index = line_index
    #         if lines_height_max < line_h: lines_height_max = line_h

    #     # stop increasing font size when max height is reaced
    #     if lines_height_total > title_available_h: break

    #     # break in more line if lines too wide
    #     if lines_width_max > title_available_w: 
    #         # lines_num += 1
            
    #         # title_words = title.split(' ')
    #         # title_words_num = len(title_words)
    #         # lines_num = lines_num
    #         # line_words_num = title_words_num // lines_num
    #         # lines = []
    #         # line = []
    #         # for i, word in enumerate(title_words):
    #         #     if len(line) < line_words_num:
    #         #         line.append(word)
    #         #     else:
    #         #         line.append(word)
    #         #         lines.append(' '.join(line))
    #         #         line = []
    #         # lines.append(' '.join(line))
    #         # i = 1
    #         pass
    #     else:
    #         i += 1

    for i in range(999):
        title_font_size = i
        title_font = ImageFont.truetype(font_text, title_font_size)

        words = title.split()
        lines = []
        line = ''
        for word in words:
            _, _, line_w, line_h = title_font.getbbox(line)
            _, _, word_w, word_h = title_font.getbbox(word)
            if line_w + word_w < title_available_w:
                line += f'{word} '
            else:
                lines.append(line.strip())
                line = f'{word} '
        lines.append(line.strip())

        lines_height_total = 0
        for line_index, line in enumerate(lines):
            _, _, line_w, line_h = title_font.getbbox(line)
            lines_height_total += line_h
        if lines_height_total > title_available_h: break

    print(lines)

    for i in range(999):
        title_font_size -= 1
        title_font = ImageFont.truetype(font_text, title_font_size)

        lines_height_total = 0
        for line_index, line in enumerate(lines):
            _, _, line_w, line_h = title_font.getbbox(line)
            lines_height_total += line_h
        if lines_height_total < title_available_h: break


    for i, line in enumerate(lines):
        draw.text((x_1, y_1 + (title_font_size * i)), line, title_color, font=title_font)



def a4_draw_title_constrained_y_new(draw, grid_map, title):
    # GET TITLE BOX
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

    print(row_i_1, col_i_1, row_i_2, col_i_2)
    
    x_1 = g.A4_CELL_SIZE * col_i_1
    y_1 = g.A4_CELL_SIZE * row_i_1
    x_2 = g.A4_CELL_SIZE * (col_i_2 + 1)
    y_2 = g.A4_CELL_SIZE * (row_i_2 + 1)

    print(x_1, y_1, x_2, y_2)
    
    title_available_w = x_2 - x_1
    title_available_h = y_2 - y_1

    print(title_available_w, title_available_h)

    title = 'From Mold to Gold: The Amazing Benefits of Ozone Treatment for Grain Preservation and Quality Control'
    title_color = '#000000'
    font_size = 128
    title_font = ImageFont.truetype(font_text, font_size)
    words = title.split(' ')
    lines = []
    line = ''
    print(words)
    for word in words:
        _, _, line_w, line_h = title_font.getbbox(line)
        _, _, word_w, word_h = title_font.getbbox(word)
        if line_w + word_w < title_available_w:
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line.strip())
    print(lines)
    for i, line in enumerate(lines):
        draw.text((x_1, y_1 + (font_size * i)), line, title_color, font=title_font)
    


def a4_draw_text_study(draw, text, grid_map, commit):
    text_total = text
    text_words_written = 0
    body_font = ImageFont.truetype(font_text, g.BODY_FONT_SIZE)

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


def cover_front(img, draw):
    # IMAGE
    cell_x = 2
    cell_y = 8

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y
    bg_image_w = g.A4_WIDTH - (g.A4_CELL_SIZE * cell_x) - (g.A4_CELL_SIZE * 2)
    bg_image_h = g.A4_HEIGHT - (g.A4_CELL_SIZE * cell_y) - (g.A4_CELL_SIZE * 2)

    images_filenames = os.listdir('C:/magazine_database/2024_06/cover/')
    foreground = Image.open(f'C:/magazine_database/2024_06/cover/{images_filenames[-1]}')
    foreground = util.img_resize(foreground, bg_image_w, bg_image_h)
    img.paste(foreground, (x, y))

    # TITLE
    cell_x = 2
    cell_y = 3

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y

    title = 'OZONOGROUP'
    font_size = 300
    font = ImageFont.truetype(font_text, font_size)
    draw.text((x, y), title, '#000000', font=font)


    # BLOCK 1

    # title
    cell_y = 10

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y

    title = 'Ozono vs. rifiuti organici delle raffinerie'
    font_size = 96
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(title)

    draw.text((g.A4_WIDTH//2 - title_w//2, y), title, '#ffffff', font=font)
    
    # desc

    cell_y = 12

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y

    font_size = 48
    text = 'Può l\'ozono risolvere l\'enorme problema della produzione di inquinamento organico da parte delle raffinerie? Nuovi studi fanno luce sulla questione.'
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(text)

    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        _, _, word_w, _ = font.getbbox(word)
        _, _, line_w, _ = font.getbbox(line)
        if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line)

    for i, line in enumerate(lines):
        _, _, line_w, _ = font.getbbox(line)
        draw.text((g.A4_WIDTH//2 - line_w//2, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    

    # BLACK OVERLAY
    x_1 = g.A4_CELL_SIZE * 5
    y_1 = g.A4_HEIGHT - g.A4_CELL_SIZE * 8
    x_2 = g.A4_WIDTH - g.A4_CELL_SIZE * 5
    y_2 = g.A4_HEIGHT - g.A4_CELL_SIZE * 3
    overlay_width = x_2 - x_1

    draw.rectangle(
        (
            (x_1, y_1), 
            (x_2, y_2)
        ), 
        fill="#000000"
    )
    

    # BLOCK 2

    # title
    x = g.A4_CELL_SIZE * 6
    y = g.A4_HEIGHT - g.A4_CELL_SIZE * 7 - (g.A4_CELL_SIZE//4)

    font_size = 64
    text = 'Addio Norovirus'
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(text)

    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        _, _, word_w, _ = font.getbbox(word)
        _, _, line_w, _ = font.getbbox(line)
        if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line)

    for i, line in enumerate(lines):
        _, _, line_w, _ = font.getbbox(line)
        draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    # desc
    x = g.A4_CELL_SIZE * 6
    y = g.A4_HEIGHT - g.A4_CELL_SIZE * 6

    font_size = 48
    text = 'Possono le microbolle eliminare i Norovirus anche se con poco ozono?'
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(text)

    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        _, _, word_w, _ = font.getbbox(word)
        _, _, line_w, _ = font.getbbox(line)
        if line_w + word_w < (overlay_width//2) - (g.A4_CELL_SIZE * 2):
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line)

    for i, line in enumerate(lines):
        draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    
    # BLOCK 3

    # title
    x = g.A4_CELL_SIZE * 18
    y = g.A4_HEIGHT - g.A4_CELL_SIZE * 7 - (g.A4_CELL_SIZE//4)

    font_size = 64
    text = 'Mangimi Sani'
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(text)

    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        _, _, word_w, _ = font.getbbox(word)
        _, _, line_w, _ = font.getbbox(line)
        if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line)

    for i, line in enumerate(lines):
        _, _, line_w, _ = font.getbbox(line)
        draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    # desc
    y = g.A4_HEIGHT - g.A4_CELL_SIZE * 6

    font_size = 48
    text = 'UVC+O3... Combinazione efficace per eliminare le microtossine nei mangimi?'
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(text)

    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        _, _, word_w, _ = font.getbbox(word)
        _, _, line_w, _ = font.getbbox(line)
        if line_w + word_w < (overlay_width//2) - (g.A4_CELL_SIZE * 2):
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    lines.append(line)

    for i, line in enumerate(lines):
        draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    

def cover_back(img, draw):
    # IMAGE
    cell_x = 2
    cell_y = 8

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y
    w = g.A4_WIDTH - (g.A4_CELL_SIZE * 2)
    h = g.A4_HEIGHT - (g.A4_CELL_SIZE * 2)

    # images_filenames = os.listdir('C:/magazine_database/2024_06/cover/')
    # foreground = Image.open(f'C:/magazine_database/2024_06/cover/{images_filenames[-1]}')
    # foreground = util.img_resize(foreground, bg_image_w, bg_image_h)
    # img.paste(foreground, (x, y))

    draw.rectangle(
        (
            (x, y), 
            (w, h)
        ), 
        fill="#c6d9d8"
    )


    

    # title
    cell_y = 34

    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y

    title = 'OZONOGROUP SRL'
    font_size = 96
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(title)

    draw.text((g.A4_WIDTH//2 - title_w//2, y), title, '#000000', font=font)
    
    cell_y += 2
    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y
    title = 'Telefono: +39 0423 952833'
    font_size = 48
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(title)
    draw.text((g.A4_WIDTH//2 - title_w//2, y), title, '#000000', font=font)
    
    cell_y += 1
    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y
    title = 'Email: info@ozonogroup.it'
    font_size = 48
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(title)
    draw.text((g.A4_WIDTH//2 - title_w//2, y), title, '#000000', font=font)
    
    cell_y += 1
    x = g.A4_CELL_SIZE * cell_x
    y = g.A4_CELL_SIZE * cell_y
    title = 'Sito Web: www.ozonogroup.it'
    font_size = 48
    font = ImageFont.truetype(font_text, font_size)
    _, _, title_w, _ = font.getbbox(title)
    draw.text((g.A4_WIDTH//2 - title_w//2, y), title, '#000000', font=font)
    


    # # desc

    # cell_y = 12

    # x = g.A4_CELL_SIZE * cell_x
    # y = g.A4_CELL_SIZE * cell_y

    # font_size = 48
    # text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque tempus, orci ultrices fermentum posuere, nulla nibh gravida ligula, vel fringilla arcu ex eu neque.'
    # font = ImageFont.truetype(font_text, font_size)
    # _, _, title_w, _ = font.getbbox(text)

    # words = text.split(' ')
    # lines = []
    # line = ''
    # for word in words:
    #     _, _, word_w, _ = font.getbbox(word)
    #     _, _, line_w, _ = font.getbbox(line)
    #     if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
    #         line += f'{word} '
    #     else:
    #         lines.append(line.strip())
    #         line = f'{word} '
    # lines.append(line)

    # for i, line in enumerate(lines):
    #     _, _, line_w, _ = font.getbbox(line)
    #     draw.text((g.A4_WIDTH//2 - line_w//2, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    

    # # BLACK OVERLAY
    # x_1 = g.A4_CELL_SIZE * 5
    # y_1 = g.A4_HEIGHT - g.A4_CELL_SIZE * 8
    # x_2 = g.A4_WIDTH - g.A4_CELL_SIZE * 5
    # y_2 = g.A4_HEIGHT - g.A4_CELL_SIZE * 3
    # overlay_width = x_2 - x_1

    # draw.rectangle(
    #     (
    #         (x_1, y_1), 
    #         (x_2, y_2)
    #     ), 
    #     fill="#000000"
    # )
    

    # # BLOCK 2

    # # title
    # x = g.A4_CELL_SIZE * 6
    # y = g.A4_HEIGHT - g.A4_CELL_SIZE * 7 - (g.A4_CELL_SIZE//4)

    # font_size = 64
    # text = 'Cassiopeia'
    # font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    # _, _, title_w, _ = font.getbbox(text)

    # words = text.split(' ')
    # lines = []
    # line = ''
    # for word in words:
    #     _, _, word_w, _ = font.getbbox(word)
    #     _, _, line_w, _ = font.getbbox(line)
    #     if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
    #         line += f'{word} '
    #     else:
    #         lines.append(line.strip())
    #         line = f'{word} '
    # lines.append(line)

    # for i, line in enumerate(lines):
    #     _, _, line_w, _ = font.getbbox(line)
    #     draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    # # desc
    # x = g.A4_CELL_SIZE * 6
    # y = g.A4_HEIGHT - g.A4_CELL_SIZE * 6

    # font_size = 48
    # text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque tempus.'
    # font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    # _, _, title_w, _ = font.getbbox(text)

    # words = text.split(' ')
    # lines = []
    # line = ''
    # for word in words:
    #     _, _, word_w, _ = font.getbbox(word)
    #     _, _, line_w, _ = font.getbbox(line)
    #     if line_w + word_w < (overlay_width//2) - (g.A4_CELL_SIZE * 2):
    #         line += f'{word} '
    #     else:
    #         lines.append(line.strip())
    #         line = f'{word} '
    # lines.append(line)

    # for i, line in enumerate(lines):
    #     draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    
    # # BLOCK 3

    # # title
    # x = g.A4_CELL_SIZE * 18
    # y = g.A4_HEIGHT - g.A4_CELL_SIZE * 7 - (g.A4_CELL_SIZE//4)

    # font_size = 64
    # text = 'Genimi'
    # font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    # _, _, title_w, _ = font.getbbox(text)

    # words = text.split(' ')
    # lines = []
    # line = ''
    # for word in words:
    #     _, _, word_w, _ = font.getbbox(word)
    #     _, _, line_w, _ = font.getbbox(line)
    #     if line_w + word_w < bg_image_w - (g.A4_CELL_SIZE * 8):
    #         line += f'{word} '
    #     else:
    #         lines.append(line.strip())
    #         line = f'{word} '
    # lines.append(line)

    # for i, line in enumerate(lines):
    #     _, _, line_w, _ = font.getbbox(line)
    #     draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
    # # desc
    # y = g.A4_HEIGHT - g.A4_CELL_SIZE * 6

    # font_size = 48
    # text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque tempus.'
    # font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    # _, _, title_w, _ = font.getbbox(text)

    # words = text.split(' ')
    # lines = []
    # line = ''
    # for word in words:
    #     _, _, word_w, _ = font.getbbox(word)
    #     _, _, line_w, _ = font.getbbox(line)
    #     if line_w + word_w < (overlay_width//2) - (g.A4_CELL_SIZE * 2):
    #         line += f'{word} '
    #     else:
    #         lines.append(line.strip())
    #         line = f'{word} '
    # lines.append(line)

    # for i, line in enumerate(lines):
    #     draw.text((x, y + (font_size * i * 1.3)), line, '#ffffff', font=font)
    
