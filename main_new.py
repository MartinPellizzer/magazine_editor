
import os
import csv
import json
import time
import random
from PIL import Image, ImageDraw, ImageFont

import g
import util
import util_ai
import mag

page_x = g.WINDOW_WIDTH//2-g.PAGE_WIDTH//2
page_y = g.WINDOW_HEIGHT//2-g.PAGE_HEIGHT//2

font_text = 'assets/fonts/Lato/Lato-Regular.ttf'

vault_folderpath = '/home/ubuntu/vault'

studies_folderpath = f'{vault_folderpath}/studies'
magazine_vol = '2024-07'
magazine_folderpath = f'{studies_folderpath}/{magazine_vol}'
magazine_pages_foldernames = os.listdir(magazine_folderpath)

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

def ai_body_sm(json_filepath, data):
    study_abstract = data['study_abstract']
    key = 'body_sm'
    # if key in data: del data[key]
    if key not in data: data[key] = []
    if data[key] == []:
        good_reply = False
        while not good_reply:
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
                line = line.strip()
                if line.lower().startswith('paragrafo'):
                    if paragraph_curr != '':
                        if paragraph_curr.endswith('.'):
                            paragraphs.append(paragraph_curr)
                            paragraph_curr = ''
                else:
                    paragraph_curr += line
            if paragraph_curr != '':
                if paragraph_curr.endswith('.'):
                    paragraphs.append(paragraph_curr)
            if len(paragraphs) == 5:
                print('*********************************************************')
                print(paragraphs)
                print('*********************************************************')
                data[key] = paragraphs
                util.json_write(json_filepath, data)
                good_reply = True
            time.sleep(g.SLEEP_TIME)


def ai_body_lg(json_filepath, data):
    key = 'body_lg'
    # if key in data: del data[key]
    if key not in data: data[key] = []
    if data[key] == []:
        paragraphs = data['body_sm']
        for paragraph in paragraphs:
            good_prompt = False
            while not good_prompt:
                prompt = f'''
                    Scrivi 1 paragrafo dettagliato usando i seguenti dati: {paragraph}
                    Rispondi in meno di 160 parole.
                    Rispondi in 1 paragrafo.
                    Non scrivere liste.
                '''
                reply = util_ai.gen_reply(prompt).strip()
                words_num = len(reply.split(" "))
                print(f'num words text = {words_num}')
                if reply != '' and words_num < 240:
                    print('*********************************************************')
                    print(reply)
                    print('*********************************************************')
                    data[key].append(reply)
                    util.json_write(json_filepath, data)
                    good_prompt = True
                time.sleep(g.SLEEP_TIME)


def ai_title_sm(json_filepath, data):
    key = 'title_sm'
    # if key in data: del data[key]
    if key not in data:
        study_abstract = data['body_sm']
        prompt = f'''
            Scrivi in Italiano un titolo corto che attiri l'attenzione per il seguente articolo: {study_abstract}
            Rispondi in meno di 5 parole.
        '''
        reply = util_ai.gen_reply(prompt).strip()

        if len(reply.split(' ')) <= 9:
            print('*********************************************************')
            print(reply)
            print('*********************************************************')
            data[key] = reply
            util.json_write(json_filepath, data)
        time.sleep(g.SLEEP_TIME)


####################################################################################################
# COVER
####################################################################################################


def magazine_cover_front():
    magazine_cover_filepath_out = f'export/{magazine_vol}/0000.jpg'
    if not os.path.exists(magazine_cover_filepath_out): return
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    mag.cover_front(img, draw)
    img.save(magazine_cover_filepath_out)
    # img.show()
    # quit()



def magazine_cover_back():
    magazine_cover_filepath_out = f'export/{magazine_vol}/9999.jpg'
    if not os.path.exists(magazine_cover_filepath_out): return
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    mag.cover_back(img, draw)
    img.save(magazine_cover_filepath_out)
    # img.show()
    # quit()


def draw_page_num(draw, grid_map, page_index):
    # page num
    font_size = 32
    font = ImageFont.truetype(font_text, font_size)
    y_1 = g.A4_HEIGHT - g.A4_CELL_SIZE*2 
    color = '#000000'
    if page_index % 2 != 0:
        text = f'{page_index}   OZONOGROUP'
        x_1 = g.A4_CELL_SIZE*2 
        if 'd' in grid_map[-2][2]: color = '#ffffff'
    else:
        text = f'OZONOGROUP   {page_index}'
        _, _, text_w, _ = font.getbbox(text)
        x_1 = g.A4_WIDTH - g.A4_CELL_SIZE*2 - text_w
        color = '#ffffff'
        if 'd' in grid_map[-2][-2]: color = '#ffffff'
    draw.text((x_1, y_1), text, color, font=font)


####################################################################################################
# EXE
####################################################################################################

def main():
    export_index = 0
    '''
    templates_filepaths = [
        f'templates/{filename}' for filename in os.listdir('templates') if filename.endswith('.csv')
    ]
    '''
    template_url = 'templates/0001.csv'
    magazine_foldername = '2024-07'
    magazine_folderpath = f'{vault_folderpath}/studies/{magazine_foldername}'
    articles_folderpath = f'{magazine_folderpath}/articles'
    clusters_foldernames = os.listdir(articles_folderpath)
    page_index = 1
    page_full_index = 0
    for cluster_foldername in clusters_foldernames:
        cluster_folderpath = f'{articles_folderpath}/{cluster_foldername}'
        articles_foldernames = os.listdir(cluster_folderpath)
        for article_foldername in articles_foldernames:
            article_folderpath = f'{cluster_folderpath}/{article_foldername}'
            grid_map = []
            with open(template_url, "r") as f:
                reader = csv.reader(f)
                for i, line in enumerate(reader):
                    grid_map.append(line)
            # page_1
            page_1 = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
            draw = ImageDraw.Draw(page_1)
            # title
            title = 'insert a very very very long title here'
            mag.a4_draw_title_constrained_y_new(draw, grid_map, title)
            # body
            with open(f'{article_folderpath}/content.txt') as f: content = f.read()
            lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line == '': continue
                if line.endswith(':'): continue
                if line.startswith('**'): continue
                if line.lower().startswith('paragraph'): continue
                lines.append(line)
            text = '\n'.join(lines)
            mag.a4_draw_text_study(draw, text, grid_map, commit=True)
            draw_page_num(draw, grid_map, page_index)
            # save
            try: os.makedirs(f'export/{magazine_foldername}')
            except: pass
            page_1.save(f'export/{magazine_foldername}/{page_index}.jpg')
            page_index += 1

            # page_2
            page_2 = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
            draw = ImageDraw.Draw(page_2)
            # image
            magazine_image_folderpath = f'assets/test-images/image-0000.png'
            print(magazine_image_folderpath)
            foreground = Image.open(magazine_image_folderpath)
            foreground = util.img_resize(foreground, g.A4_WIDTH, g.A4_HEIGHT)
            page_2.paste(foreground, (0, 0))
            # page num
            draw_page_num(draw, grid_map, page_index)
            # save
            try: os.makedirs(f'export/{magazine_foldername}')
            except: pass
            page_2.save(f'export/{magazine_foldername}/{page_index}.jpg')
            page_index += 1

            # page_full
            page_full = Image.new('RGB', (g.A4_WIDTH*2, g.A4_HEIGHT), color='white')
            draw = ImageDraw.Draw(page_full)
            foreground = Image.open(f'export/{magazine_foldername}/{page_index-2}.jpg')
            page_full.paste(foreground, (0, 0))
            foreground = Image.open(f'export/{magazine_foldername}/{page_index-1}.jpg')
            page_full.paste(foreground, (g.A4_WIDTH, 0))
            # page_full.show()
            try: os.makedirs(f'export/{magazine_foldername}')
            except: pass
            page_full_filepath = f'export/{magazine_foldername}/_{page_full_index}.jpg'
            page_full.save(page_full_filepath)
            page_full_index += 1
            quit()


def main_old():
    page_i = 0
    for magazine_page_foldername in magazine_pages_foldernames:
        if magazine_page_foldername == 'cover': continue
        if magazine_page_foldername[0] == '_': continue
        page_i += 1
        
        # TODO: debug, to comment 
        # if page_i < 4: continue 

        magazine_page_folderpath = f'{magazine_folderpath}/{magazine_page_foldername}'
        print(magazine_page_folderpath)
        quit()

        # data    
        json_filepath = f'{magazine_page_folderpath}/data.json'
        with open(json_filepath, 'r', encoding='utf-8') as f: 
            data = json.load(f)

        # GENERATE ARTICLE "CHUNKS"
        ai_body_sm(json_filepath, data)
        ai_body_lg(json_filepath, data)
        ai_title_sm(json_filepath, data)

        templates_filepaths = [f'templates/{filename}' for filename in os.listdir('templates') if filename.endswith('.csv')]
        template_url = random.choice(templates_filepaths)
        
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

        study_title = data['title_sm'].replace('\"', '')
        mag.a4_draw_title_constrained_y(draw, grid_map, study_title)

        paragraphs_body_small = [paragraph.replace('\n', ' ').strip() for paragraph in data['body_sm']]
        paragraphs_body_large = [paragraph.replace('\n', ' ').strip() for paragraph in data['body_lg']]

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

        paragraphs[paragraph_index-1] = paragraphs_body_small[paragraph_index-1]
        for paragraph in paragraphs:
            print(paragraph)
            print()

        text = '\n'.join(paragraphs)
        mag.a4_draw_text_study(draw, text, grid_map, commit=True)

        # page num
        font_size = 32
        font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
        y_1 = g.A4_HEIGHT - g.A4_CELL_SIZE*2 
        color = '#000000'
        if page_i % 2 != 0:
            text = f'{page_i}   OZONOGROUP'
            x_1 = g.A4_CELL_SIZE*2 
            if 'd' in grid_map[-2][2]: color = '#ffffff'
        else:
            text = f'OZONOGROUP   {page_i}'
            _, _, text_w, _ = font.getbbox(text)
            x_1 = g.A4_WIDTH - g.A4_CELL_SIZE*2 - text_w
            if 'd' in grid_map[-2][-2]: color = '#ffffff'
        draw.text((x_1, y_1), text, color, font=font)

        export_id = ''
        if page_i < 10: export_id = f'000{page_i}'
        elif page_i < 100: export_id = f'00{page_i}'
        elif page_i < 1000: export_id = f'0{page_i}'
        elif page_i < 10000: export_id = f'{page_i}'

        if not os.path.exists(f'export/{magazine_vol}'):
            os.makedirs(f'export/{magazine_vol}')
        img.save(f'export/{magazine_vol}/{export_id}.jpg')
        # img.show()
        # quit()
        
main()
# main_old()
quit()

magazine_cover_front()
magazine_cover_back()

def merge_pdf():
    images = [
        Image.open(f"export/{magazine_vol}/{filename}")
        for filename in os.listdir(f"export/{magazine_vol}/")
        if filename.endswith('.jpg')
    ]

    pdf_path = f'export/{magazine_vol}/_magazine.pdf'
    images[0].save(
        pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=images[1:]
    )

merge_pdf()
