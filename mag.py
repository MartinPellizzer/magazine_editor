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
            foreground = Image.open(f"{img_folder}/{i}.jpg")
            fg_w = x_2 - x_1
            fg_h = y_2 - y_1
            foreground = util.img_resize(foreground, fg_w, fg_h)
            img.paste(foreground, (x_1, y_1))





def a4_draw_text(draw, text, grid_map):
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

            text = text.replace(line, '').strip()
            if not is_last_line:
                words = line.split(" ")
                words_length = sum(draw.textlength(w, font=body_font) for w in words)
                space_length = (((line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE) - words_length) / (len(words) - 1)
                x = x_1
                for word in words:
                    draw.text((x, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), word, font=body_font, fill=c_body)
                    x += draw.textlength(word, font=body_font) + space_length
            else:
                draw.text((x_1, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), line, c_body, font=body_font)
                break

            text_words_written += len(line.split(' '))

        if is_last_line: break

    text_words_total = len(text_total.split(' '))
    print(f'text words total: {text_words_total}')
    print(f'text words written: {text_words_written}')
    print(f'text words overflow: {text_words_total-text_words_written}')



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

    is_under = False
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

            text = text.replace(line, '').strip()
            if not is_last_line:
                words = line.split(" ")
                words_length = sum(draw.textlength(w, font=body_font) for w in words)
                space_length = (((line_coord[3] - line_coord[1]) * g.A4_CELL_SIZE) - words_length) / (len(words) - 1)
                x = x_1
                for word in words:
                    if commit: draw.text((x, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), word, font=body_font, fill=c_body)
                    x += draw.textlength(word, font=body_font) + space_length
            else:
                if commit: draw.text((x_1, y_1 + (g.BODY_FONT_SIZE * 1.3 * i)), line, c_body, font=body_font)
                break

            text_words_written += len(line.split(' '))

        if is_last_line: 
            is_under = True
            break
    

    text_words_total = len(text_total.split(' '))
    print(f'text words total: {text_words_total}')
    print(f'text words written: {text_words_written}')


    return is_under