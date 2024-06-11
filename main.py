
import os
import csv
import json
from PIL import Image, ImageDraw, ImageFont

a4_w = 2480
a4_h = 3508


window_w = 1280
window_h = 720

page_w = 248*2
page_h = 351*2
page_x = window_w//2-page_w//2
page_y = window_h//2-page_h//2

body_font_size = 30
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", body_font_size)


# load json data
json_filepath = 'database/2024_06/page_0001.json'
with open(json_filepath, 'r', encoding='utf-8') as f: 
    data = json.load(f)

json_template_filepath = 'templates/2024_06/0001.json'
with open(json_template_filepath, 'r', encoding='utf-8') as f: 
    data_template = json.load(f)

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


img = Image.new('RGB', (a4_w, a4_h), color='white')
draw = ImageDraw.Draw(img)


# TODO: load csv and gen a4 pdf (magazine)

grid_map = []
template_url = data['template_url']
with open(template_url, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        grid_map.append(row)


page_grid_col_num = 16 
page_grid_col_w = page_w / page_grid_col_num

page_grid_row_num = 16 
page_grid_row_h = page_h / page_grid_row_num

# page_guides_col_num = 3 
# page_guides_col_padding = page_grid_col_w*4
# page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num


page_guides_col_num = data_template['col_num']
page_guides_col_padding = page_grid_col_w*4
page_guides_col_w = (page_w - page_guides_col_padding) / page_guides_col_num


page_guides_row_num = 12
page_guides_row_padding = page_grid_row_h*4
page_guides_row_h = (page_h - page_guides_row_padding) / page_guides_row_num



a4_grid_row_num = page_grid_row_num
a4_grid_row_h = a4_h / a4_grid_row_num

a4_grid_col_num = page_grid_col_num
a4_grid_col_w = a4_w / a4_grid_col_num

a4_guides_col_num = page_guides_col_num
a4_guides_col_padding = a4_grid_col_w*4
a4_guides_col_gap = 16
a4_guides_col_w = (a4_w - a4_guides_col_padding) / a4_guides_col_num

a4_guides_row_num = page_guides_row_num
a4_guides_row_padding = a4_grid_row_h*4
a4_guides_row_h = (a4_h - a4_guides_row_padding) / a4_guides_row_num


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

    image_url = data['image_url']
    foreground = Image.open(image_url)
    fg_w = x_2 - x_1
    fg_h = y_2 - y_1
    foreground = img_resize(foreground, fg_w, fg_h)
    img.paste(foreground, (x_1, y_1))


# draw title
title = data['title']
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


# draw body
body = data['body']
text = body.replace('\n', ' ')


cols_i_list = []
if page_guides_col_num == 1:
    cols_i_list = [2]
elif page_guides_col_num == 2:
    cols_i_list = [2, 8]
elif page_guides_col_num == 3:
    cols_i_list = [2, 6, 10]

blocks_list = []
block_curr = ['', '', '']
for col_i in range(a4_grid_col_num):
    if col_i in cols_i_list:
        for row_i in range(a4_grid_row_num):
            # print(f'{col_i}:{row_i} -> {grid_map[row_i][col_i]}')
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


export_url = data['export_url']
img.save(export_url)
# img.show()
