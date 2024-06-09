from PIL import Image, ImageDraw, ImageFont
import random
import csv


body_font_size = 30
body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", body_font_size)

def cell_pos(col_index, row_index):
    x = grid_col_w * col_index + grid_col_padding
    y = grid_row_h * row_index + grid_row_padding
    return x, y


def draw_grid():
    for i in range(grid_col_num+1):
        draw.line((grid_col_w*i + grid_col_padding, 0, grid_col_w*i + grid_col_padding, page_h), fill='#ff00ff', width=4)
        draw.line((grid_col_w*i + grid_col_padding - grid_col_gap, 0, grid_col_w*i + grid_col_padding - grid_col_gap, page_h), fill='#ff00ff', width=4)
        draw.line((grid_col_w*i + grid_col_padding + grid_col_gap, 0, grid_col_w*i + grid_col_padding + grid_col_gap, page_h), fill='#ff00ff', width=4)

    for i in range(grid_row_num+1):
        draw.line((0, grid_row_h*i + grid_row_padding, page_w, grid_row_h*i + grid_row_padding), fill='#ff00ff', width=4)


def draw_grid_num():
    font_size = 72
    font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

    for i in range(grid_col_num):
        for k in range(grid_row_num):
            x = grid_col_w*i + grid_col_padding
            y = grid_row_h*k + grid_row_padding
            draw.text((x, y), f'{k}:{i}', '#ff00ff', font=font)


def text_to_lines(text):
    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        _, _, line_curr_w, _ = body_font.getbbox(line_curr)
        _, _, word_w, _ = body_font.getbbox(word)
        if line_curr_w + word_w < grid_col_w - grid_col_gap*2:
            line_curr += f'{word} '
        else:
            lines.append(line_curr)
            line_curr = f'{word} '
    lines.append(line_curr)
    
    return lines 


def draw_text_col(text, col_index, row_index):
    lines = text_to_lines(text)

    for i, line in enumerate(lines):
        x = grid_col_w*col_index + grid_col_padding + grid_col_gap*col_index
        y = grid_row_h*row_index + grid_row_padding + font_size*i
        draw.text((x, y), line, (0, 0, 0), font=font)




grid_map = []
with open('map.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        grid_row = []
        for item in row:
            grid_row.append(int(item))
        grid_map.append(grid_row)

print(grid_map)

page_w = 2480
page_h = 3508

img = Image.new('RGB', (page_w, page_h), color='white')
draw = ImageDraw.Draw(img) 

# grid
grid_col_num = 3
grid_col_padding = 256
grid_col_gap = 16
grid_col_w = (page_w - grid_col_padding*2) // grid_col_num

grid_row_num = 16
grid_row_padding = 512
grid_row_h = (page_h - grid_row_padding*2) // grid_row_num

# draw_grid()
# draw_grid_num()

# grid_map = []
# for _ in range(grid_row_num):
#     row = []
#     for _ in range(grid_col_num):
#         row.append(0)
#     grid_map.append(row)



# images

# for i in range(5):
#     rand_col_num = random.randint(0, grid_col_num-1)
#     rand_row_num = random.randint(0, grid_row_num-1)
#     # rand_col_num = 0 # TODO: remove
#     # rand_row_num = 8 # TODO: remove
#     x_1 = grid_col_w * rand_col_num + grid_col_padding
#     y_1 = grid_row_h * rand_row_num + grid_row_padding

#     rand_col_span = random.randint(1, grid_col_num - rand_col_num)
#     rand_row_span = random.randint(1, grid_row_num - rand_row_num)
#     # rand_col_span = 1 # TODO: remove
#     # rand_row_span = 2 # TODO: remove
#     x_2 = x_1 + grid_col_w * rand_col_span
#     y_2 = y_1 + grid_row_h * rand_row_span

#     draw.rectangle(((x_1, y_1), (x_2, y_2)), fill="#cdcdcd")

#     for y in range(rand_row_num, rand_row_num + rand_row_span):
#         for x in range(rand_col_num, rand_col_num + rand_col_span):
#             grid_map[y][x] = 1

# print()
# for row in grid_map:
#     print(row)



# text

# def draw_text_col_around(start_row_i, start_col_i):
#     with open('demo_article.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
#     text = text.replace('\n', ' ')

#     lines = text_to_lines(text)

#     curr_line_i = 0
#     curr_col_i = start_col_i
#     curr_line_i = start_row_i
#     for _ in lines:
#         y = grid_row_h*start_row_i + grid_row_padding + body_font_size*curr_line_i
#         if y > grid_row_h*grid_row_num + grid_row_padding: 
#             curr_col_i += 1
#             curr_line_i = start_row_i

#         x = grid_col_w*curr_col_i + grid_col_padding + grid_col_gap*curr_col_i
#         y = grid_row_h*start_row_i + grid_row_padding + body_font_size*curr_line_i

#         # line_row_i = (y - grid_row_padding) // grid_row_h
#         # if line_row_i < grid_row_num and curr_col_i < grid_col_num:
#         #     if grid_map[line_row_i][curr_col_i] == 0:
#         line = lines[curr_line_i]
#         draw.text((x, y), line, (0, 0, 0), font=body_font)

#         curr_line_i += 1

# draw_text_col_around(3, 0)







# def draw_text_block(start_col_i, start_row_i, spawn_i):

#     line_i = 0
#     for _ in lines:
#         x_1 = grid_col_w*start_col_i + grid_col_padding + grid_col_gap*start_col_i
#         y_1 = grid_row_h*start_row_i + grid_row_padding + body_font_size*line_i
        
#         line_row_i = (y_1 - grid_row_padding) // grid_row_h
#         if line_row_i - start_row_i > spawn_i - 1: return 

#         draw.text((x_1, y_1), lines[line_i], (0, 0, 0), font=body_font)
#         line_i += 1

# draw_text_block(1, 2, 3)





def draw_text_blocks(text, blocks_list):
    lines = text_to_lines(text)

    block_i = 0

    start_row_i = blocks_list[block_i][0]
    start_col_i = blocks_list[block_i][1]
    end_row_i = blocks_list[block_i][2]

    line_i = 0
    for line in lines:
        x_1 = grid_col_w*start_col_i + grid_col_padding + grid_col_gap*start_col_i
        y_1 = grid_row_h*start_row_i + grid_row_padding + body_font_size*line_i

        line_row_i = (y_1 - grid_row_padding) // grid_row_h
        if line_row_i > end_row_i - 1: 
            block_i += 1
            if block_i < len(blocks_list):
                start_row_i = blocks_list[block_i][0]
                start_col_i = blocks_list[block_i][1]
                end_row_i = blocks_list[block_i][2]
                line_i = 0
                x_1 = grid_col_w*start_col_i + grid_col_padding + grid_col_gap*start_col_i
                y_1 = grid_row_h*start_row_i + grid_row_padding + body_font_size*line_i
            else:
                return

        draw.text((x_1, y_1), line, (0, 0, 0), font=body_font)
        line_i += 1


def map_to_blocks():
    blocks_list = []
    block_curr = [-1, -1, -1]
    for k in range(grid_col_num):
        for i in range(grid_row_num):
            if grid_map[i][k] == 0:
                if block_curr[0] == -1: block_curr[0] = i
                if block_curr[1] == -1: block_curr[1] = k
            elif grid_map[i][k] == 1:
                if block_curr != [-1, -1, -1]:
                    if block_curr[2] == -1: block_curr[2] = i
                    blocks_list.append(block_curr)
                    block_curr = [-1, -1, -1]
        if block_curr != [-1, -1, -1]:
            if block_curr[2] == -1: block_curr[2] = i
            blocks_list.append(block_curr)
            block_curr = [-1, -1, -1]
    return blocks_list




with open('demo_article.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
text = text.replace('\n', ' ')

blocks_list = [
    [2, 0, 7],
    [10, 0, 13],
    [0, 1, 4],
    [7, 1, 10],
    [11, 2, 15],
]

# blocks_list = [
#     [0, 0, 5], 
#     [11, 0, 15], 
#     [0, 1, 5], 
#     [11, 1, 15], 
#     [0, 2, 15]
# ]

blocks_list = map_to_blocks()

draw_text_blocks(text, blocks_list)

# draw_text_col_around(0, 1)
# draw_text_col_around(0, 2)

# font_size = 30
# font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

# for i in range(grid_row_num):
#     for k in range(grid_col_num):
#         if grid_map[i][k] == 0:
#             x, y = cell_pos(k, i)
#             draw.text((x, y), text, '#000', font=font)


# with open('placeholder_text.txt', 'r', encoding='utf-8', errors='ignore') as f: text = f.read()
# text = text.replace('\n', ' ')

# draw_text_col(text, 0, 0)
# draw_text_col(text, 1, 8)
# draw_text_col(text, 2, 3)


# draw_text_col(lines[:32], 0, rand_rows + 1)





img.show()
# img.save('test.jpg')