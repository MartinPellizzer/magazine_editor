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

mo = 300*margin_mul
mt = 500*margin_mul
mi = 500*margin_mul
mb = 800*margin_mul

p1_ml = mo
p1_mt = mt
p1_mr = mi
p1_mb = mb

p2_ml = mi
p2_mt = mt
p2_mr = mo
p2_mb = mb

col_num = 2
col_w = (a4_w - p1_mr - p1_ml) / col_num

row_num = 4
row_h = (a4_h - p1_mt - p1_mb) / row_num

line_num = 13
line_spacing = 1.3
line_h = row_h / line_num


font_size = line_h / line_spacing
body_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica.ttf', font_size)

a4_col_gap = line_h * 2
a4_row_gap = line_h * line_spacing

map_matrix = []
for i in range(row_num):
    row = []
    for j in range(col_num):
        row.append('')
    map_matrix.append(row)

def image_gen(prompt, image_filepath_out):
    image = pipe(prompt=prompt, num_inference_steps=25).images[0]
    image.save(image_filepath_out)

def draw_page(page_num, body_text, place='left', image_regen=False, show_guides=False):
    if place == 'left':
        text_area_x1 = p1_ml
        text_area_y1 = p1_mt
        text_area_x2 = a4_w - p1_mr
        text_area_y2 = a4_h - p1_mb
        text_area_w = text_area_x2 - text_area_x1
        text_area_h = text_area_y2 - text_area_y1
    else:
        text_area_x1 = p2_ml
        text_area_y1 = p2_mt
        text_area_x2 = a4_w - p2_mr
        text_area_y2 = a4_h - p2_mb
        text_area_w = text_area_x2 - text_area_x1
        text_area_h = text_area_y2 - text_area_y1

    for i in range(row_num):
        for j in range(col_num):
            map_matrix[i][j] = ''

    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)

    ## draw guides
    if 0:
        for i in range(row_num):
            for j in range(line_num+1):
                draw.line((text_area_x1, text_area_y1 + row_h*i + line_h*j, text_area_x2, text_area_y1 + row_h*i + line_h*j), fill='#00ff00', width=4)

        for i in range(col_num+1):
            draw.line((text_area_x1 + col_w*i, text_area_y1, text_area_x1 + col_w*i, text_area_y2), fill='#00ffff', width=4)
            draw.line((text_area_x1 + col_w*i - line_h, text_area_y1, text_area_x1 + col_w*i - line_h, text_area_y2), fill='#00ffff', width=4)

        for i in range(row_num+1):
            draw.line((text_area_x1, text_area_y1 + row_h*i, text_area_x2, text_area_y1 + row_h*i), fill='#00ffff', width=4)
            draw.line((text_area_x1, text_area_y1 + row_h*i - line_h, text_area_x2, text_area_y1 + row_h*i - line_h), fill='#00ffff', width=4)

        draw.line((text_area_x1, text_area_y1, text_area_x2, text_area_y1), fill='#ff0000', width=4)
        draw.line((text_area_x1, text_area_y2, text_area_x2, text_area_y2), fill='#ff0000', width=4)
        draw.line((text_area_x1, text_area_y1, text_area_x1, text_area_y2), fill='#ff0000', width=4)
        draw.line((text_area_x2, text_area_y1, text_area_x2, text_area_y2), fill='#ff0000', width=4)

    ## images
    total_cells = 0
    image_index = 0
    for image_i in range(99):
        if image_regen:
            prompt = f'''
                milk,
                food photography,
                natural light, 
                depth of field, bokeh,
                high resolution, cinematic
            '''
            image_gen(prompt, 'images/image-1.png')

        if image_index == 0:
            cell_x1_index = random.randint(0, col_num-1)
            cell_y1_index = random.randint(0, row_num-1)
            cell_x2_index = random.randint(cell_x1_index, col_num-1)
            cell_y2_index = random.randint(cell_y1_index, row_num-1)
        else:
            available_cells = []
            for i in range(row_num):
                for j in range(col_num):
                    if map_matrix[i][j] == '':
                        available_cells.append([i, j])
            random_cell = random.choice(available_cells)
            cell_x1_index = random_cell[1]
            cell_y1_index = random_cell[0]
            cell_x2_index = random_cell[1]
            cell_y2_index = random_cell[0]

        print(f'{cell_x1_index}:{cell_y1_index}')
        print(f'{cell_x2_index}:{cell_y2_index}')

        selected_cells = (cell_x2_index - cell_x1_index + 1) * (cell_y2_index - cell_y1_index + 1)
        print(selected_cells)
        if total_cells == 3: break
        if total_cells + selected_cells > 3: continue
        total_cells += selected_cells
        
        ## update map_matrix
        if image_index == 0:
            for i in range(row_num):
                for j in range(col_num):
                    if i >= cell_y1_index and j >= cell_x1_index and i <= cell_y2_index and j <= cell_x2_index:
                        map_matrix[i][j] = f'i_{image_index}'
        else:
            map_matrix[cell_y1_index][cell_x1_index] = f'i_{image_index}'
        image_index += 1
        for row in map_matrix:
            print(row)
        
        ## resize/draw image
        x1 = int(text_area_x1 + col_w * cell_x1_index)
        y1 = int(text_area_y1 + row_h * cell_y1_index)
        w = int(col_w * (cell_x2_index - cell_x1_index + 1) - line_h)
        h = int(row_h * (cell_y2_index - cell_y1_index + 1) - line_h - (line_h - line_h/line_spacing))
        print(x1, y1, w, h)
        util.img_resize_save(
            'images/image-1.png', 'images/image-1-resized.jpg', 
            w=w, h=h, 
            quality=100,
        )
        foreground = Image.open('images/image-1-resized.jpg')
        img.paste(foreground, (x1, y1))
        print()

        ## text blocks
        blocks = []
        for i in range(col_num):
            for j in range(row_num):
                # print(f'col: {i}, row: {j} - {map_matrix[j][i]}')
                if map_matrix[j][i] == '':
                    blocks.append([i, j])

    ## title
    '''
    title_text = 'Come l\'ozono elimina l\'aspergillus nel formaggio montasio'
    a4_title_font_size = line_h*2
    a4_title_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica-Bold.ttf', a4_title_font_size)

    title_lines = []
    line_curr = ''
    for word in title_text.split(' '):
        _, _, line_curr_w, _ = a4_title_font.getbbox(line_curr)
        _, _, word_w, _ = a4_title_font.getbbox(word)
        if line_curr_w + word_w < col_w - a4_col_gap:
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
            x1 = text_area_x1 + col_w*block_curr_x
            y1 = text_area_y1 + row_h*block_curr_y
            y_line = y1 + (a4_title_font_size*i*line_spacing)
            draw.text((x1, y_line), line, '#000000', font=a4_title_font)
            i += 1
    '''
    
    ## body
    paragraphs = body_text.strip().split('\n')
    lines = []
    for paragraph in paragraphs:
        line_curr = ''
        for word in paragraph.split(' '):
            _, _, line_curr_w, _ = body_font.getbbox(line_curr)
            _, _, word_w, _ = body_font.getbbox(word)
            if line_curr_w + word_w < col_w - a4_col_gap:
                line_curr += f'{word} '
            else:
                lines.append(line_curr.strip())
                line_curr = f'{word} '
        lines.append(line_curr.strip())

    if len(blocks) != 0:
        block_index = 0
        block_curr_x, block_curr_y = blocks[block_index]

        block_x = text_area_x1 + col_w*block_curr_x
        block_y = text_area_y1 + row_h*block_curr_y
        line_i = 0
        for i, line in enumerate(lines):
            line_x = block_x
            line_y = block_y + font_size*line_i*line_spacing
            next_line_y = block_y + font_size*(line_i+1)*line_spacing
            ## change block
            if line_i >= line_num: 
                ## if no more blocks available to fit content -> cutoff
                if block_index+1 >= len(blocks): break
                line_i = 0
                block_index += 1
                block_curr_x, block_curr_y = blocks[block_index]
                block_x = text_area_x1 + col_w*block_curr_x
                block_y = text_area_y1 + row_h*block_curr_y
                line_x = block_x
                line_y = block_y + font_size*line_i*line_spacing
            else:
                if line_i + 1 == line_num:
                    ## if no more blocks available to fit content -> cutoff
                    if block_index+1 >= len(blocks): break
                    if blocks[block_index+1][1] - blocks[block_index][1] != 1:
                        line_i = 0
                        block_index += 1
                        block_curr_x, block_curr_y = blocks[block_index]
                        block_x = text_area_x1 + col_w*block_curr_x
                        block_y = text_area_y1 + row_h*block_curr_y
                        line_x = block_x
                        line_y = block_y + font_size*line_i*line_spacing

            if i < len(lines) - 1 and lines[i+1] == '':
                ## last line of paragraph
                draw.text((line_x, line_y), line, '#000000', font=body_font)
            elif i == len(lines) - 1:
                ## last line of text
                draw.text((line_x, line_y), line, '#000000', font=body_font)
            else:
                ## align-justify
                word_x = block_x
                _, _, line_w, _ = body_font.getbbox(line)
                space_left = col_w - line_h - line_w
                words = line.split(' ')
                word_num = len(words)
                if word_num - 1 > 0: space_add = space_left / (word_num-1)
                else: space_add = 0
                for word in words:
                    draw.text((word_x, line_y), word, '#000000', font=body_font)
                    _, _, word_w, _ = body_font.getbbox(word)
                    _, _, space_w, _ = body_font.getbbox(' ')
                    word_x += word_w + space_w + space_add

            line_i += 1
                
            # quit()

    ## check avg words per line
    words_sum = len(body_text.split(' '))
    avg_len = words_sum / len(lines)
    print(avg_len)

    line = 'page 1'
    x1 = text_area_x1
    y1 = text_area_y2 + (line_h*line_spacing*8)
    draw.text((x1, y1), line, '#000000', font=body_font)

    img.save(f'exports-test/{page_num}.jpg')
    # img.show()
    # quit()

def draw_page_full_image(image_i, place='left', image_regen=False):
    if place == 'left':
        text_area_x1 = p1_ml
        text_area_y1 = p1_mt
        text_area_x2 = a4_w - p1_mr
        text_area_y2 = a4_h - p1_mb
        text_area_w = text_area_x2 - text_area_x1
        text_area_h = text_area_y2 - text_area_y1
    else:
        text_area_x1 = p2_ml
        text_area_y1 = p2_mt
        text_area_x2 = a4_w - p2_mr
        text_area_y2 = a4_h - p2_mb
        text_area_w = text_area_x2 - text_area_x1
        text_area_h = text_area_y2 - text_area_y1

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
    _, _, line_w, _ = body_font.getbbox(line)
    x1 = text_area_x2 - line_w
    y1 = text_area_y2 + (line_h*line_spacing*8)
    draw.text((x1, y1), line, '#ffffff', font=body_font)

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
for i in range(100):
    draw_page(f'{i}', body_text, 'left', image_regen=False, show_guides=False)
    # draw_page_full_image('2', 'right', image_regen=False)
    # draw_page_double('1', '2')
    # quit()
quit()

def magazine_gen(image_i):
    draw_page(image_i, 'right')
    draw_page_full_image(image_i)


for image_i in range(100):
    magazine_gen(image_i)
    quit()

