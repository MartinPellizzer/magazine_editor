
import os
import csv
import json
import time
from PIL import Image, ImageDraw, ImageFont

import g
import util
import util_ai
import mag

page_x = g.WINDOW_WIDTH//2-g.PAGE_WIDTH//2
page_y = g.WINDOW_HEIGHT//2-g.PAGE_HEIGHT//2



####################################################################################################
# FUNC
####################################################################################################


def a4_draw_title(draw):
    title = 'Nature\'s \nWonderland'
    title_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", g.TITLE_FONT_SIZE)
    title_col_i = ''
    title_row_i = ''
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
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
    for row_i in range(g.GRID_ROW_NUM):
        for col_i in range(g.GRID_COL_NUM):
            if grid_map[row_i][col_i] == 't':
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i

    title_available_w = (col_i_2 - col_i_1 + 1) * a4_grid_col_w
    title_available_h = (row_i_2 - row_i_1 + 1) * a4_grid_row_h

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


# TODO: function dark backgroud for white text
def draw_dark():
    pass



####################################################################################################
# AI
####################################################################################################

def ai_body_small(json_filepath, data):
    key = 'body_small'
    # if key in data: del data[key]
    if key not in data:
        prompt = f'''
            Scrivi in Italiano 5 paragrafi brevi dettagliati usando i dati provenienti dall'abstract del seguente studio scientifico: {study_abstract}.

            Nel paragrafo 1, scrivi l'introduzione in 100 parole.
            Nel paragrafo 2, scrivi i metodi in 100 parole.
            Nel paragrafo 3, scrivi i risultati in 100 parole.
            Nel paragrafo 4, scrivi le discussioni in 100 parole.
            Nel paragrafo 5, scrivi le conclusioni in 100 parole.

            Per i paragrafi usa i seguenti titoli: Paragrafo 1, Paragrafo 2, Paragrafo 3, Paragrafo 4, Paragrafo 5.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        lines = reply.split('\n')
        paragraphs = []
        paragraph_curr = ''
        for line in lines:
            # print(line)
            line = line.strip()
            if line.lower().startswith('paragrafo'):
                if paragraph_curr != '':
                    paragraphs.append(paragraph_curr)
                    paragraph_curr = ''
            else:
                paragraph_curr += line
        if paragraph_curr != '':
            paragraphs.append(paragraph_curr)

        if len(paragraphs) == 5:
            print('*********************************************************')
            print(paragraphs)
            print('*********************************************************')
            data[key] = paragraphs
            util.json_write(json_filepath, data)
        time.sleep(g.SLEEP_TIME)


def ai_body_large(json_filepath, data):
    key = 'body_large'
    # if key in data: del data[key]
    if key not in data:
        data[key] = []
        paragraphs = data['body_small']
        for paragraph in paragraphs:
            good_prompt = False
            while not good_prompt:
                # prompt = f'''
                #     Riscrivi il seguente paragrafo rendendolo di poco più lungo: {paragraph}
                #     Rispondi in meno di 150 parole.
                #     Rispondi in 1 paragrafo.
                #     Non scrivere liste.
                # '''
                prompt = f'''
                    Scrivi 1 paragrafo dettagliato usando i seguenti dati: {paragraph}
                    
                    Rispondi in meno di 150 parole.
                    Rispondi in 1 paragrafo.
                    Non scrivere liste.
                '''
                reply = util_ai.gen_reply(prompt).strip()

                words_num = len(reply.split(" "))
                print(f'num words text = {words_num}')
                if reply != '' and words_num < 200:
                    print('*********************************************************')
                    print(reply)
                    print('*********************************************************')
                    data[key].append(reply)
                    util.json_write(json_filepath, data)
                    good_prompt = True
                time.sleep(g.SLEEP_TIME)



####################################################################################################
# EXE
####################################################################################################
magazine_vol = '2024_06'
magazine_folderpath = f'database/{magazine_vol}'
magazine_pages_foldernames = os.listdir(magazine_folderpath)
i = 0
for magazine_page_foldername in magazine_pages_foldernames:
    if i < 10:
        i += 1
        continue 
    magazine_page_folderpath = f'{magazine_folderpath}/{magazine_page_foldername}'
    print(magazine_page_folderpath)

    # data    
    json_filepath = f'{magazine_page_folderpath}/data.json'
    with open(json_filepath, 'r', encoding='utf-8') as f: 
        data = json.load(f)

    # GENERATE ARTICLE "CHUNKS"
    study_journal = data['study_journal']
    study_abstract = data['study_abstract']

    ai_body_small(json_filepath, data)
    ai_body_large(json_filepath, data)

    template_url = data['template_url']
    print(template_url)
    
    # TODO: remve or manage log of page without template
    if not os.path.exists(template_url): continue

    # template
    grid_map = []
    with open(template_url, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            grid_map.append(line)

    # magazine
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    try: mag.a4_draw_images(img, magazine_page_folderpath, grid_map)
    except: pass

    mag.a4_draw_dark(draw, grid_map)

    paragraphs_body_small = [paragraph.replace('\n', ' ').strip() for paragraph in data['body_small']]
    paragraphs_body_large = [paragraph.replace('\n', ' ').strip() for paragraph in data['body_large']]

    text = ''
    paragraphs = [paragraph for paragraph in paragraphs_body_small]

    paragraph_index = 0
    text_overflow = False
    for _ in range(5):
        text = '\n'.join(paragraphs)

        is_under = mag.a4_draw_text_study(draw, text, grid_map, commit=False)

        if is_under: 
            paragraphs[paragraph_index] = paragraphs_body_large[paragraph_index]
        else: 
            text_overflow = True
            break
        
        paragraph_index += 1

    if text_overflow:
        paragraphs[paragraph_index-1] = paragraphs_body_small[paragraph_index-1]


    # TODO: ottimizza scelta paragrafi per riempire i buchi
        # Scorri il primo array (small) x numero volte di elementi del secondo array (large)
        # in un singolo scorrimento, sostituisci uno alla volta gli elementi in small con large
        # ogni nuovo scorrimento, comincia a scorre da un elemento in avanti e i precedenti mettili tutti a large

    for paragraph in paragraphs:
        print(paragraph)
        print()

    text = '\n'.join(paragraphs)
    mag.a4_draw_text_study(draw, text, grid_map, commit=True)

    study_title = data['study_title']
    # study_title = "Nature's \nWonderland"
    mag.a4_draw_title_new(draw, grid_map, study_title)
    
    # mag.a4_draw_grid(draw)


    export_url = data['export_url']
    img.save(export_url)
    # img.show()

    # quit()
