import os
import json
import random

from PIL import Image, ImageDraw, ImageFont
from lorem_text import lorem

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler

from oliark import json_read, json_write
from oliark_llm import llm_reply

import util

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

a4_col_gap = line_h
a4_row_gap = line_h * line_spacing

map_matrix = []
for i in range(row_num):
    row = []
    for j in range(col_num):
        row.append('')
    map_matrix.append(row)

def draw_page(page_i, title_text, body_text, images, place='left', show_guides=False):
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
        for row in map_matrix:
            print(row)
        
        ## resize/draw image
        x1 = int(text_area_x1 + col_w * cell_x1_index)
        y1 = int(text_area_y1 + row_h * cell_y1_index)
        w = int(col_w * (cell_x2_index - cell_x1_index + 1) - line_h)
        h = int(row_h * (cell_y2_index - cell_y1_index + 1) - line_h - (line_h - line_h/line_spacing))
        print(x1, y1, w, h)
        print(images)
        print(image_index)
        util.img_resize_save(
            f'images/{images[image_index]}.png', f'images/{images[image_index]}-resized.jpg', 
            w=w, h=h, 
            quality=100,
        )
        foreground = Image.open(f'images/{images[image_index]}-resized.jpg')
        img.paste(foreground, (x1, y1))
        print()

        ## text blocks
        blocks = []
        for i in range(col_num):
            for j in range(row_num):
                # print(f'col: {i}, row: {j} - {map_matrix[j][i]}')
                if map_matrix[j][i] == '':
                    blocks.append([i, j])
        image_index += 1

    ## title
    # title_text = 'Come l\'ozono elimina l\'aspergillus nel formaggio montasio'
    title_font_size = font_size*2
    title_font = ImageFont.truetype(f'{vault_folderpath}/fonts/helvetica/Helvetica-Bold.ttf', title_font_size)

    title_lines = []
    line = ''
    for word in title_text.split(' '):
        _, _, line_w, _ = title_font.getbbox(line)
        _, _, word_w, _ = title_font.getbbox(word)
        if line_w + word_w < col_w - line_h:
            line += f'{word} '
        else:
            title_lines.append(line.strip())
            line = f'{word} '
    title_lines.append(line.strip())

    if len(blocks) != 0:
        block_index = 0
        block_curr_x, block_curr_y = blocks[block_index]
        i = 0
        x1 = text_area_x1 + col_w*block_curr_x
        y1 = text_area_y1 + row_h*block_curr_y
        for line in title_lines:
            y_line = y1 + (title_font_size*i*line_spacing)
            draw.text((x1, y_line), line, '#000000', font=title_font)
            i += 1
    paragraph_offset_y = title_font_size*i*line_spacing + (font_size*line_spacing)
    paragraph_lines_done = len(title_lines)*2  + 1
    
    ## body
    body_text = body_text.strip().replace('\n', ' ').replace('  ', ' ')
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
            line_y += paragraph_offset_y
            next_line_y = block_y + font_size*(line_i+1)*line_spacing
            ## change block
            if line_i >= line_num - paragraph_lines_done: 
                ## if no more blocks available to fit content -> cutoff
                if block_index+1 >= len(blocks): break
                line_i = 0
                block_index += 1
                block_curr_x, block_curr_y = blocks[block_index]
                block_x = text_area_x1 + col_w*block_curr_x
                block_y = text_area_y1 + row_h*block_curr_y
                line_x = block_x
                line_y = block_y + font_size*line_i*line_spacing
                paragraph_offset_y = 0
                paragraph_lines_done = 0
            else:
                if line_i + 1 == line_num - paragraph_lines_done:
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
                        paragraph_offset_y = 0
                        paragraph_lines_done = 0

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

    line = str(page_i)
    x1 = text_area_x1
    y1 = text_area_y2 + (line_h*line_spacing*8)
    draw.text((x1, y1), line, '#000000', font=body_font)

    img.save(f'exports-test/{page_i}.jpg')
    # img.show()
    # quit()


def draw_page_full_image(page_i, images, place='left'):
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

    img = Image.new('RGB', (a4_w, a4_h), color='white')
    draw = ImageDraw.Draw(img)
    util.img_resize_save(
        f'images/{images[0]}.png', f'images/{images[0]}-resized.jpg', 
        w=a4_w, h=a4_h, 
        quality=100,
    )
    foreground = Image.open(f'images/{images[0]}-resized.jpg')
    img.paste(foreground, (0, 0))

    line = str(page_i)
    _, _, line_w, _ = body_font.getbbox(line)
    x1 = text_area_x2 - line_w
    y1 = text_area_y2 + (line_h*line_spacing*8)
    draw.text((x1, y1), line, '#ffffff', font=body_font)

    img.save(f'exports-test/{page_i}.jpg')
    # img.show()


def draw_page_double(image_i_1, image_i_2):
    img = Image.new('RGB', (a4_w*2, a4_h), color='white')
    draw = ImageDraw.Draw(img)
    foreground_1 = Image.open(f'exports-test/{image_i_1}.jpg')
    foreground_2 = Image.open(f'exports-test/{image_i_2}.jpg')
    img.paste(foreground_1, (0, 0))
    img.paste(foreground_2, (a4_w, 0))
    img.show()


##############################################################
# get study text
##############################################################

news_num = 0
study_num = 0
studies_filepaths = []
news_folderpath = f'{vault_folderpath}/ozonogroup/news/done'
for news_filename in os.listdir(news_folderpath):
    news_filepath = f'{news_folderpath}/{news_filename}'
    news_dict = json_read(news_filepath)
    news_year = int(news_dict['year'])
    news_month = int(news_dict['month'])
    news_category = news_dict['category']
    if news_year == 2024 and news_month == 8:
        if news_category == 'sanificazione':
            news_num += 1
            study_filepath = f'{vault_folderpath}/ozonogroup/studies/pubmed/ozone/json/{news_filename}'
            if os.path.exists(study_filepath):
                studies_filepaths.append(study_filepath)
                study_num += 1

for study_filepath in studies_filepaths:
    print(study_filepath)
print(news_num)
print(study_num)
print(news_num - study_num)

## gen images (stable diffustion)
if 0:
    ## stable diffusion init
    checkpoint_filepath = '/home/ubuntu/vault/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
    pipe = StableDiffusionXLPipeline.from_single_file(
        checkpoint_filepath, 
        torch_dtype=torch.float16, 
        use_safetensors=True, 
        variant="fp16"
    ).to('cuda')
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    page_i = 0
    for study_filepath in studies_filepaths[:]:
        study_filename = study_filepath.split('/')[-1]
        study = json_read(study_filepath)
        article = study['PubmedArticle'][0]['MedlineCitation']['Article']
        title_text = article['ArticleTitle']
        abstract_text = article['Abstract']['AbstractText']
        abstract_text = ' '.join(abstract_text)

        with open('tags.txt') as f: tags_all = f.read()
        prompt = f'''
            Give me the 4 most relevant tags from the following list of TAGS related to the following ARTICLE.
            Reply in the following JSON format:
            {{
                "tag1": "name tag 1",
                "tag2": "name tag 2",
                "tag3": "name tag 3",
                "tag4": "name tag 4"
            }}
            Reply only with the json, don't add additional content.
            Choose the tags only from the list of tags, don't invent them.
            In case you can't find relevant tags from the list of tags, reply "NA" for the tags names.
            TAGS: {tags_all}
            ARTICLE: {abstract_text}
        '''
        reply = llm_reply(prompt)
        reply_dict = json.loads(reply)

        with open('tags-food.txt') as f: tags_support = f.read()
        tags_support = tags_support.split('\n')
        prompt1 = reply_dict['tag1'] + ', ' + ', '.join(tags_support)
        prompt2 = reply_dict['tag2'] + ', ' + ', '.join(tags_support)
        prompt3 = reply_dict['tag3'] + ', ' + ', '.join(tags_support)
        prompt4 = reply_dict['tag4'] + ', ' + ', '.join(tags_support)
        print(prompt1)
        print(prompt2)
        print(prompt3)
        print(prompt4)
        images_prompts = [prompt1, prompt2, prompt3, prompt4]
        for image_i, image_prompt in enumerate(images_prompts):
            if not os.path.exists(f'images/{page_i}-image-{image_i}.png'):
                image = pipe(prompt=image_prompt, num_inference_steps=25).images[0]
                image.save(f'images/{page_i}-image-{image_i}.png')

        page_i += 2

## gen text
else:
    page_i = 0
    for study_filepath in studies_filepaths[:]:
        study_filename = study_filepath.split('/')[-1]
        study = json_read(study_filepath)
        article = study['PubmedArticle'][0]['MedlineCitation']['Article']
        title_text = article['ArticleTitle']
        abstract_text = article['Abstract']['AbstractText']
        abstract_text = ' '.join(abstract_text)

        if not os.path.exists(f'jsons/{study_filename}'):
            with open(f'jsons/{study_filename}', 'w', encoding='utf-8') as f:
                f.write('{}')
        data = json_read(f'jsons/{study_filename}')

        key = 'title'
        if key not in data:
            for i in range(99):
                prompt = f'''
                    Write a title in less than 7 words for the following scientific STUDY in a easy to understandable way.
                    Reply with the following JSON format:
                    {{
                        "title": "<write title here>"
                    }}
                    Write only the json, don't add additional content.
                    Don't include tags, only plain text.
                    Include the word "ozone" in the title if relevant.
                    STUDY: {title_text} \n{abstract_text}
                '''
                reply = llm_reply(prompt)
                try: reply_dict = json.loads(reply)
                except: continue
                break
            title_text = reply_dict['title']
            data[key] = title_text
            json_write(f'jsons/{study_filename}', data)

        key = 'body'
        if key not in data:
            for i in range(99):
                prompt = f'''
                    Write a 400 words article to explain the following scientific STUDY in a easy to understandable way.
                    The article must be 4 paragraphs.
                    In paragraph 1, write an introduction to the study, explaining why the subject of the matter is important.
                    In paragraph 2, write the methods used.
                    In paragraph 3, write the results achieved.
                    In paragraph 4, write the conclusion.
                    Reply with the following JSON format:
                    {{
                        "introduction": "<write introduction here>",
                        "methods": "<write methods here>",
                        "results": "<write results here>",
                        "conclusion": "<write conclusion here>"
                    }}
                    Don't add titles and subtitles, write only the paragraphs.
                    Don't include tags, only plain text.
                    STUDY: {abstract_text}
                '''
                reply = llm_reply(prompt)
                try: reply_dict = json.loads(reply)
                except: continue
                break
            introduction = reply_dict['introduction']
            methods = reply_dict['methods']
            results = reply_dict['results']
            conclusion = reply_dict['conclusion']
            body_text = f'{introduction} {methods} {results} {conclusion}'
            data[key] = body_text
            json_write(f'jsons/{study_filename}', data)

        title_text = data['title']
        body_text = data['body']
        rand_side = random.choice([0, 1])
        print('rand side', rand_side)
        if rand_side == 0:
            images = [f'{page_i}-image-1', f'{page_i}-image-2', f'{page_i}-image-3']
            draw_page(f'{page_i}', title_text, body_text, images, 'left', show_guides=False)
            images = [f'{page_i}-image-0']
            draw_page_full_image(page_i+1, images, 'right')
        else:
            images = [f'{page_i}-image-0']
            draw_page_full_image(page_i, images, 'left')
            images = [f'{page_i}-image-1', f'{page_i}-image-2', f'{page_i}-image-3']
            draw_page(f'{page_i+1}', title_text, body_text, images, 'right', show_guides=False)
        page_i += 2

