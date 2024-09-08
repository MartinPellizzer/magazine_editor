import random

from PIL import Image, ImageDraw, ImageFont
from lorem_text import lorem

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler

import util

## stable diffusion init
'''
checkpoint_filepath = '/home/ubuntu/vault/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
'''

vault_folderpath = '/home/ubuntu/vault'

# body_text = lorem.words(1200)
a4_w = 2480
a4_h = 3508

margin_mul = 0.75

a4_mo = int(300*margin_mul)
a4_mt = int(500*margin_mul)
a4_mi = int(500*margin_mul)
a4_mb = int(800*margin_mul)

a4_p1_ml = a4_mo
a4_p1_mt = a4_mt
a4_p1_mr = a4_mi
a4_p1_mb = a4_mb

a4_p2_ml = a4_mi
a4_p2_mt = a4_mt
a4_p2_mr = a4_mo
a4_p2_mb = a4_mb

a4_col_num = 2
a4_col_w = (a4_w - a4_p1_mr - a4_p1_ml) / a4_col_num

a4_row_num = 4
a4_row_h = (a4_h - a4_p1_mt - a4_p1_mb) / a4_row_num

a4_body_lines_num = 15
a4_body_line_spacing = 1.2
a4_body_font_size = a4_row_h / a4_body_lines_num
a4_body_font_size /= a4_body_line_spacing



# TODO: remove
# a4_body_font_size = 28
# a4_body_line_spacing = 1.1 
print('row_h:', a4_row_h)
print('lines_num:', a4_body_lines_num)
print('font_size:', a4_body_font_size)
print('row_h:', a4_body_font_size * a4_body_lines_num)
# quit()

a4_col_gap = a4_body_font_size * 2
a4_row_gap = a4_body_font_size * a4_body_line_spacing
a4_body_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica.ttf', a4_body_font_size)

map_matrix = []
for i in range(a4_row_num):
    row = []
    for j in range(a4_col_num):
        row.append('')
    map_matrix.append(row)

def image_gen(prompt, image_filepath_out):
    image = pipe(prompt=prompt, num_inference_steps=25).images[0]
    image.save(image_filepath_out)

def draw_page(image_i, body_text, place='left', image_regen=False, show_guides=False):
    if place == 'left':
        a4_text_area_x1 = a4_p1_ml
        a4_text_area_y1 = a4_p1_mt
        a4_text_area_x2 = a4_w - a4_p1_mr
        a4_text_area_y2 = a4_h - a4_p1_mb
        a4_text_area_w = a4_text_area_x2 - a4_text_area_x1
        a4_text_area_h = a4_text_area_y2 - a4_text_area_y1
    else:
        a4_text_area_x1 = a4_p2_ml
        a4_text_area_y1 = a4_p2_mt
        a4_text_area_x2 = a4_w - a4_p2_mr
        a4_text_area_y2 = a4_h - a4_p2_mb
        a4_text_area_w = a4_text_area_x2 - a4_text_area_x1
        a4_text_area_h = a4_text_area_y2 - a4_text_area_y1

    for i in range(a4_row_num):
        for j in range(a4_col_num):
            map_matrix[i][j] = ''

    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)

    ## draw guides
    if show_guides:
        x1 = a4_text_area_x1
        y1 = a4_text_area_y1
        x2 = a4_text_area_x2
        y2 = y1
        draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
        x1 = a4_text_area_x1
        y1 = a4_text_area_y2
        x2 = a4_text_area_x2
        y2 = y1
        draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
        x1 = a4_text_area_x1
        y1 = a4_text_area_y1
        x2 = x1
        y2 = a4_text_area_y2
        draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
        x1 = a4_text_area_x2
        y1 = a4_text_area_y1
        x2 = x1
        y2 = a4_text_area_y2
        draw.line((x1, y1, x2, y2), fill='#ff0000', width=4)
        for i in range(a4_col_num+1):
            if i == 0: continue
            x1 = a4_text_area_x1 + a4_col_w*i
            y1 = a4_text_area_y1
            x2 = x1
            y2 = a4_text_area_y2
            draw.line((x1, y1, x2, y2), fill='#00ffff', width=4)
            draw.line((x1 - a4_col_gap, y1, x2 - a4_col_gap, y2), fill='#00ffff', width=4)
        for i in range(a4_row_num+1):
            if i == 0: continue
            x1 = a4_text_area_x1
            y1 = a4_text_area_y1 + a4_row_h*i
            x2 = a4_text_area_x2 
            y2 = y1
            draw.line((x1, y1, x2, y2), fill='#00ffff', width=4)
            draw.line((x1, y1 - a4_row_gap, x2, y2 - a4_row_gap), fill='#00ffff', width=4)

    ## images
    if image_regen:
        prompt = f'''
            milk,
            food photography,
            natural light, 
            depth of field, bokeh,
            high resolution, cinematic
        '''
        image_gen(prompt, 'images/image-1.png')

    foreground = Image.open('images/image-1.png')
    cell_x1_index = random.randint(0, a4_col_num-1)
    cell_y1_index = random.randint(0, a4_row_num-1)
    cell_x2_index = random.randint(cell_x1_index, a4_col_num-1)
    cell_y2_index = random.randint(cell_y1_index, a4_row_num-1)
    print(f'{cell_x1_index}:{cell_y1_index}')
    print(f'{cell_x2_index}:{cell_y2_index}')
    print()
    for i in range(a4_row_num):
        for j in range(a4_col_num):
            if i >= cell_y1_index and j >= cell_x1_index and i <= cell_y2_index and j <= cell_x2_index:
                map_matrix[i][j] = 'i_0'

    for row in map_matrix:
        print(row)
    
    x1 = int(a4_text_area_x1 + a4_col_w * cell_x1_index)
    y1 = int(a4_text_area_y1 + a4_row_h * cell_y1_index)
    w = int(a4_col_w * (cell_x2_index - cell_x1_index + 1) - a4_col_gap)
    h = int(a4_row_h * (cell_y2_index - cell_y1_index + 1) - a4_row_gap*1.2)

    util.img_resize_save(
        'images/image-1.png', 'images/image-1-resized.jpg', 
        w=w, h=h, 
        quality=100,
    )
    foreground = Image.open('images/image-1-resized.jpg')
    img.paste(foreground, (x1, y1))

    ## text blocks
    blocks = []
    for i in range(a4_col_num):
        for j in range(a4_row_num):
            print(f'col: {i}, row: {j} - {map_matrix[j][i]}')
            if map_matrix[j][i] == '':
                blocks.append([i, j])

    ## title
    title_text = 'Come l\'ozono elimina l\'aspergillus nel formaggio montasio'
    a4_title_font_size = a4_body_font_size*2
    a4_title_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica-Bold.ttf', a4_title_font_size)

    title_lines = []
    line_curr = ''
    for word in title_text.split(' '):
        _, _, line_curr_w, _ = a4_title_font.getbbox(line_curr)
        _, _, word_w, _ = a4_title_font.getbbox(word)
        if line_curr_w + word_w < a4_col_w - a4_col_gap:
            line_curr += f'{word} '
        else:
            title_lines.append(line_curr.strip())
            line_curr = f'{word} '
    title_lines.append(line_curr.strip())

    if len(blocks) != 0:
        block_index = 0
        block_curr_x, block_curr_y = blocks[block_index]
        i = 0
        for line in title_lines:
            x1 = a4_text_area_x1 + a4_col_w*block_curr_x
            y1 = a4_text_area_y1 + a4_row_h*block_curr_y
            y_line = y1 + (a4_title_font_size*i*a4_body_line_spacing)
            draw.text((x1, y_line), line, '#000000', font=a4_title_font)
            i += 1
    
    ## body
    paragraphs = body_text.strip().split('\n')
    lines = []
    for paragraph in paragraphs:
        line_curr = ''
        for word in paragraph.split(' '):
            _, _, line_curr_w, _ = a4_body_font.getbbox(line_curr)
            _, _, word_w, _ = a4_body_font.getbbox(word)
            if line_curr_w + word_w < a4_col_w - a4_col_gap:
                line_curr += f'{word} '
            else:
                lines.append(line_curr.strip())
                line_curr = f'{word} '
        lines.append(line_curr.strip())

    if len(blocks) != 0:
        block_index = 0
        block_curr_x, block_curr_y = blocks[block_index]
        i = 0
        for line_i, line in enumerate(lines):
            x1 = a4_text_area_x1 + a4_col_w*block_curr_x

            ## manage 1st block with title
            if block_index == 0:
                y1 = a4_text_area_y1 + a4_row_h*block_curr_y + (a4_title_font_size*a4_body_line_spacing*len(title_lines)) + (a4_body_font_size*a4_body_line_spacing)
                block_h = a4_row_h - (a4_title_font_size*a4_body_line_spacing*len(title_lines)) - (a4_body_font_size*a4_body_line_spacing)
                if block_index+1 < len(blocks):
                    if blocks[block_index+1][1] - block_curr_y != 1:
                        block_h -= a4_body_font_size*a4_body_line_spacing
                else:
                    block_h -= a4_body_font_size*a4_body_line_spacing
            else:
                y1 = a4_text_area_y1 + a4_row_h*block_curr_y
                ## if not last block
                if block_index+1 < len(blocks):
                    ## if not contiguous block
                    if blocks[block_index+1][1] - block_curr_y != 1:
                        block_h = a4_row_h - a4_body_font_size*a4_body_line_spacing
                    else:
                        block_h = a4_row_h
                ## if last block
                else:
                    block_h = a4_row_h - a4_body_font_size*a4_body_line_spacing

            y_line = y1 + (a4_body_font_size*i*a4_body_line_spacing)

            if y_line - y1 >= block_h:
                block_index += 1
                i = 0
                if block_index >= len(blocks): break
                block_curr_x, block_curr_y = blocks[block_index]
                x1 = a4_text_area_x1 + a4_col_w*block_curr_x
                y1 = a4_text_area_y1 + a4_row_h*block_curr_y
                y_line = y1 + (a4_body_font_size*i*a4_body_line_spacing)

            print(line)
            if line_i == len(lines)-1:
                draw.text((x1, y_line), line, '#000000', font=a4_body_font)
            else:
                words = line.split(' ')
                word_x_curr = x1
                _, _, line_w, _ = a4_body_font.getbbox(line)
                empty_space = a4_col_w - a4_col_gap - line_w
                if len(words) - 1 > 0: 
                    adding_space = empty_space / (len(words)-1)
                else:
                    adding_space = 0
                if lines[line_i+1] == '':
                    draw.text((x1, y_line), line, '#000000', font=a4_body_font)
                else:
                    for word in words:
                        _, _, word_w, _ = a4_body_font.getbbox(word)
                        _, _, space_w, _ = a4_body_font.getbbox(' ')
                        draw.text((word_x_curr, y_line), word, '#000000', font=a4_body_font)
                        word_x_curr += word_w + space_w + adding_space

            # quit()
            i += 1

    ## check avg words per line
    words_sum = len(body_text.split(' '))
    avg_len = words_sum / len(lines)
    print(avg_len)

    line = 'page 1'
    x1 = a4_text_area_x1
    y1 = a4_text_area_y2 + (a4_body_font_size*a4_body_line_spacing*8)
    draw.text((x1, y1), line, '#000000', font=a4_body_font)

    img.save(f'exports-test/{image_i}.jpg')
    # img.show()

def draw_page_full_image(image_i, place='left', image_regen=False):
    if place == 'left':
        a4_text_area_x1 = a4_p1_ml
        a4_text_area_y1 = a4_p1_mt
        a4_text_area_x2 = a4_w - a4_p1_mr
        a4_text_area_y2 = a4_h - a4_p1_mb
        a4_text_area_w = a4_text_area_x2 - a4_text_area_x1
        a4_text_area_h = a4_text_area_y2 - a4_text_area_y1
    else:
        a4_text_area_x1 = a4_p2_ml
        a4_text_area_y1 = a4_p2_mt
        a4_text_area_x2 = a4_w - a4_p2_mr
        a4_text_area_y2 = a4_h - a4_p2_mb
        a4_text_area_w = a4_text_area_x2 - a4_text_area_x1
        a4_text_area_h = a4_text_area_y2 - a4_text_area_y1

    if image_regen:
        prompt = f'''
            cheese,
            food photography,
            natural light, 
            depth of field, bokeh,
            high resolution, cinematic
        '''
        image_gen(prompt, 'images/image-0.png')

    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)
    util.img_resize_save(
        'images/image-0.png', 'images/image-0-resized.jpg', 
        w=a4_w, h=a4_h, 
        quality=100,
    )
    foreground = Image.open('images/image-0-resized.jpg')
    img.paste(foreground, (0, 0))

    line = 'page 2'
    _, _, line_w, _ = a4_body_font.getbbox(line)
    x1 = a4_text_area_x2 - line_w
    y1 = a4_text_area_y2 + (a4_body_font_size*a4_body_line_spacing*8)
    draw.text((x1, y1), line, '#ffffff', font=a4_body_font)

    img.save(f'exports-test/{image_i}.jpg')
    # img.show()


def draw_page_double(image_i_1, image_i_2):
    img = Image.new('RGB', (a4_w*2, a4_h), color='white')
    draw = ImageDraw.Draw(img)
    foreground_1 = Image.open(f'exports-test/{image_i_1}.jpg')
    foreground_2 = Image.open(f'exports-test/{image_i_2}.jpg')
    img.paste(foreground_1, (0, 0))
    img.paste(foreground_2, (a4_w, 0))
    img.show()

with open('body-test.txt') as f: body_text = f.read()

# body_text = lorem.words(1200)
# body_text = body_text.strip().replace('\n', ' ').replace('  ', ' ')
draw_page('1', body_text, 'left', image_regen=False, show_guides=False)
draw_page_full_image('2', 'right', image_regen=False)
draw_page_double('1', '2')
quit()

def magazine_gen(image_i):
    draw_page(image_i, 'right')
    draw_page_full_image(image_i)


for image_i in range(100):
    magazine_gen(image_i)
    quit()

