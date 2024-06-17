
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

    # print(col_i_1, row_i_1)
    # print(col_i_2, row_i_2)

    title_available_w = (col_i_2 - col_i_1 + 1) * a4_grid_col_w
    title_available_h = (row_i_2 - row_i_1 + 1) * a4_grid_row_h
    # print(title_available_w)

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


def a4_body_blocks():
    cols_i_list = []
    if guides_col_num == 1:
        cols_i_list = [2]
    elif guides_col_num == 2:
        cols_i_list = [2, 8]
    elif guides_col_num == 3:
        cols_i_list = [2, 6, 10]
    blocks_list = []
    block_curr = ['', '', '']
    for col_i in range(g.GRID_COL_NUM):
        if col_i in cols_i_list:
            for row_i in range(g.GRID_ROW_NUM):
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
    return blocks_list


def text_to_lines(text):
    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        _, _, line_curr_w, _ = body_font.getbbox(line_curr)
        _, _, word_w, _ = body_font.getbbox(word)
        if line_curr_w + word_w < a4_guides_col_w - a4_guides_col_gap*2:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr)
    return lines


def draw_body(draw, lines, blocks_list):
    block_i = 0
    start_col_i = blocks_list[block_i][0]
    start_row_i = blocks_list[block_i][1]
    end_row_i = blocks_list[block_i][2]
    line_i = 0
    for line in lines:
        x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
        y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
        line_row_i = y_1 // a4_guides_row_h
        if line_row_i > end_row_i - 1: 
            block_i += 1
            if block_i < len(blocks_list):
                start_col_i = blocks_list[block_i][0]
                start_row_i = blocks_list[block_i][1]
                end_row_i = blocks_list[block_i][2]
                line_i = 0
                x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
                y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
            else:
                break
                
        draw.text((x_1, y_1), line, (0, 0, 0), font=body_font)
        line_i += 1


def draw_body_justify(draw, lines, blocks_list):
    block_i = 0
    start_col_i = blocks_list[block_i][0]
    start_row_i = blocks_list[block_i][1]
    end_row_i = blocks_list[block_i][2]
    line_i = 0
    lines_num = len(lines)
    for i, line in enumerate(lines):
        x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
        y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
        line_row_i = y_1 // a4_guides_row_h
        if line_row_i > end_row_i - 1: 
            block_i += 1
            if block_i < len(blocks_list):
                start_col_i = blocks_list[block_i][0]
                start_row_i = blocks_list[block_i][1]
                end_row_i = blocks_list[block_i][2]
                line_i = 0
                x_1 = a4_grid_col_w * start_col_i + a4_guides_col_gap * ((start_col_i-2)//4)
                y_1 = a4_grid_row_h * start_row_i + g.BODY_FONT_SIZE * line_i
            else:
                break

        if i != lines_num - 1:
            words = line.split(" ")
            words_length = sum(draw.textlength(w, font=body_font) for w in words)
            space_length = ((a4_guides_col_w - a4_guides_col_gap*2) - words_length) / (len(words) - 1)
            x = x_1
            for word in words:
                draw.text((x, y_1), word, font=body_font, fill="black")
                x += draw.textlength(word, font=body_font) + space_length
        else:
            draw.text((x_1, y_1), line, font=body_font, fill="black")

        line_i += 1




####################################################################################################
# EXE
####################################################################################################
magazine_vol = '2024_06'
magazine_folderpath = f'database/{magazine_vol}'
magazine_pages_foldernames = os.listdir(magazine_folderpath)
for magazine_page_foldername in magazine_pages_foldernames:
    magazine_page_folderpath = f'{magazine_folderpath}/{magazine_page_foldername}'
    print(magazine_page_folderpath)

    # data    
    json_filepath = f'{magazine_page_folderpath}/data.json'
    with open(json_filepath, 'r', encoding='utf-8') as f: 
        data = json.load(f)


    template_url = data['template_url']
    image_url = data['image_url']

    study_journal = data['study_journal']
    study_abstract = data['study_abstract']
    
    if 'body':
        key = 'body'
        # if key in data: del data[key]
        if key not in data:
            prompt = f'''
                Scrivi in Italiano 5 paragrafi dettagliati usando i dati provenienti dall'abstract del seguente studio scientifico: {study_abstract}.

                Nel paragrafo 1, scrivi l'introduzione in 400 parole.
                Nel paragrafo 2, scrivi i metodi in 400 parole.
                Nel paragrafo 3, scrivi i risultati in 400 parole.
                Nel paragrafo 4, scrivi le discussioni in 400 parole.
                Nel paragrafo 5, scrivi le conclusioni in 400 parole.
            '''
            reply = util_ai.gen_reply(prompt).strip()

            if reply != '':
                print('*********************************************************')
                print(reply)
                print('*********************************************************')
                data[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.SLEEP_TIME)


    if 'body_large':
        key = 'body_large'
        # if key in data: del data[key]
        if key not in data:
            # data[key] = []
            paragraphs = [
"L'industria dei raffinatori di petrolio utilizza notevoli quantità di acqua e genera effluenti con un'elevata contaminazione organica che non possono essere trattati nei sistemi di trattamento convenzionali. A causa della rapida crescita di queste industrie e degli effetti avversi dei loro effluenti che entrano nell'ambiente, è necessario utilizzare metodi a basso costo e ad alta efficienza. Il trattamento dell'inquinamento organico dei rifiuti delle raffinerie e di altri effluenti pericolosi mediante processi di ossidazione avanzata è diventato comune, specialmente negli ultimi decenni. Il motivo di ciò è la distruzione completa o parziale dei contaminanti in un tempo di ritenzione molto breve e con costi accettabili. Questo studio ha indagato sull'eliminazione dell'inquinamento organico (COD) dei rifiuti delle raffinerie utilizzando il metodo di ozonazione integrata/fotchimica. L'obiettivo era quello di determinare l'influenza dei parametri principali sul processo di eliminazione del COD dei rifiuti.",
"Per raggiungere l'obiettivo dello studio, sono stati condotti esperimenti di laboratorio per indagare l'influenza di quattro fattori principali, vale a dire l'importo iniziale di COD, l'input di ozono, il tempo di reazione e l'importo di catalizzatore, sull'efficienza di eliminazione del COD. Prima dell'esperimento principale, sono state eseguite prove preliminari per determinare i parametri giusti per l'esperimento. Per questo scopo, è stato utilizzato il metodo del disegno sperimentale della composizione centrale (CCD) per determinare i punti sperimentali. I dati di laboratorio sono stati quindi confrontati con l'output del modello, in modo da garantire una buona corrispondenza tra di loro. In seguito, l'ottimizzazione del processo è stata eseguita utilizzando il metodo RSM response procedure.",
"I risultati dello studio hanno mostrato che i valori ottimali delle variabili indipendenti, vale a dire il pH, COD, O3 e TiO2, sono 11, 200 mg/L, 5 g/h e 200 mg/L, rispettivamente. In queste condizioni, l'efficienza di rimozione del COD è stata del 96,3% in 50 minuti. Inoltre, è stato osservato che i cambiamenti nel livello di COD e l'input di ozono hanno un effetto significativo sull'efficienza complessiva di rimozione del COD. I risultati hanno anche dimostrato che un aumento del livello di COD e dell'input di ozono aumenta l'efficienza di rimozione del COD. Tuttavia, un aumento del livello di catalizzatore non ha avuto alcun effetto significativo sull'efficienza di rimozione del COD.",
"I risultati di questo studio hanno confermato che il metodo di ozonazione integrata/fotchimica può essere utilizzato con successo per trattare i rifiuti delle raffinerie e ridurre l'inquinamento organico. Tuttavia, i risultati hanno anche mostrato che l'efficienza del trattamento è fortemente dipendente dai livelli di COD e dall'input di ozono. Quindi, per garantire un'elevata efficienza di trattamento, è necessario mantenere i livelli di COD e l'input di ozono entro i limiti ottimali.",
"In conclusione, questo studio ha mostrato che il metodo di ozonazione integrata/fotchimica è un metodo promettente per il trattamento dei rifiuti delle raffinerie e la riduzione dell'inquinamento organico. I risultati hanno anche dimostrato che l'efficienza del trattamento è influenzata dall'importo iniziale di COD e dall'input di ozono. Pertanto, è necessario mantenere i livelli di COD e l'input di ozono entro i limiti ottimali per garantire un'elevata efficienza di trattamento. Inoltre, è importante sottolineare che i dati ottenuti in questo studio sono derivati da esperimenti di laboratorio e devono essere confermati con ulteriori ricerche su scala più ampia. Infine, il metodo utilizzato in questo studio potrebbe essere utilizzato anche per il trattamento di altri tipi di effluenti industriali con una contaminazione organica simile.",
            ]
            for paragraph in paragraphs:
                prompt = f'''
                    Espandi il seguente paragrafo: {paragraph}.
                '''
                reply = util_ai.gen_reply(prompt).strip()

                if reply != '':
                    print('*********************************************************')
                    print(reply)
                    print('*********************************************************')
                    data[key].append(reply)
                    util.json_write(json_filepath, data)
                time.sleep(g.SLEEP_TIME)

#     if 'body':
#         key = 'body'
#         # if key in data: del data[key]
#         if key not in data:
#             data[key] = []
#             sections = [
#                 '''
# I. Introduction
#     A. Explanation of Near Surface Mounted Salt Indicators (NSMSIs)
#     B. Importance of monitoring salt contamination in soil and water
#                 ''',
#                 '''
# II. Methods
#     A. Description of NSMSIs and their installation
#     B. Explanation of the study area and duration
#     C. Details of the data collection process
#                 ''',
#                 '''
# III. Results
#     A. Presentation of data on salt concentrations measured by NSMSIs
#     B. Analysis of the correlation between NSMSIs measurements and traditional sampling methods
#     C. Comparison of NSMSI performance in different soil and weather conditions
#                 ''',
#                 '''
# IV. Discussion
#     A. Interpretation of the results and their implications for soil and water contamination monitoring
#     B. Evaluation of the NSMSIs' accuracy, reliability, and cost-effectiveness
#     C. Discussion of the limitations and potential improvements of NSMSIs
#                 ''',
#                 '''
# V. Conclusion
#     A. Summary of the main findings
#     B. Implications for future research and practical applications
#     C. Significance of the study for environmental management and policy-making
#                 ''',
#             ]

#             for section in sections:
#                 prompt = f'''
#                     Scrivi in Italiano un paragrafo dettagliato utilizzando la seguente outline e i dati dal seguente studio.
#                     Outline: {section}
#                     Studio: {study_abstract}
#                 '''
#                 reply = util_ai.gen_reply(prompt).strip()

#                 if reply != '':
#                     print('*********************************************************')
#                     print(reply)
#                     print('*********************************************************')
#                     data[key].append(reply)
#                     util.json_write(json_filepath, data)
#                 time.sleep(g.SLEEP_TIME)
            

    # if 'body':
    #     key = 'body'
    #     if key in data: del data[key]
    #     if key not in data:
    #         outline = data['outline']
    #         prompt = f'''
    #             I want to write a detailed article for a scientific magazine. I'm going to give you an outline and the scientific study abstract. I want you to write a detailed paragraph for each chapter of the outline using the data from the scientific study abstract.
    #             Here's the outline: {outline} 
                                
    #             Here's the scientific study abstract: {study_abstract}
    #         '''
    #         reply = util_ai.gen_reply(prompt).strip()
    #         if reply != '':
    #             print('*********************************************************')
    #             print(reply)
    #             print('*********************************************************')
    #             data[key] = reply
    #             util.json_write(json_filepath, data)
    #         time.sleep(g.SLEEP_TIME)

    # template
    grid_map = []
    with open(template_url, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            grid_map.append(line)
            print(line)

    for line in grid_map:
        print(line)


    # magazine
    img = Image.new('RGB', (g.A4_WIDTH, g.A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    mag.a4_draw_images(img, magazine_page_folderpath, grid_map)

    text = ''
    for paragraph in data['body_large']:
        text += paragraph
    text = text.replace('\n', ' ').strip()

    paragraph_index = 0
    for _ in range(5):
        text = ''
        for paragraph in data['body_large']:
            text += paragraph
        text = text.replace('\n', ' ').strip()
        
        is_under = mag.a4_draw_text_study(draw, text, grid_map, commit=False)

        if is_under:
            key = 'body_large'
            paragraphs = [
"L'industria dei raffinatori di petrolio utilizza notevoli quantità di acqua e genera effluenti con un'elevata contaminazione organica che non possono essere trattati nei sistemi di trattamento convenzionali. A causa della rapida crescita di queste industrie e degli effetti avversi dei loro effluenti che entrano nell'ambiente, è necessario utilizzare metodi a basso costo e ad alta efficienza. Il trattamento dell'inquinamento organico dei rifiuti delle raffinerie e di altri effluenti pericolosi mediante processi di ossidazione avanzata è diventato comune, specialmente negli ultimi decenni. Il motivo di ciò è la distruzione completa o parziale dei contaminanti in un tempo di ritenzione molto breve e con costi accettabili. Questo studio ha indagato sull'eliminazione dell'inquinamento organico (COD) dei rifiuti delle raffinerie utilizzando il metodo di ozonazione integrata/fotchimica. L'obiettivo era quello di determinare l'influenza dei parametri principali sul processo di eliminazione del COD dei rifiuti.",
"Per raggiungere l'obiettivo dello studio, sono stati condotti esperimenti di laboratorio per indagare l'influenza di quattro fattori principali, vale a dire l'importo iniziale di COD, l'input di ozono, il tempo di reazione e l'importo di catalizzatore, sull'efficienza di eliminazione del COD. Prima dell'esperimento principale, sono state eseguite prove preliminari per determinare i parametri giusti per l'esperimento. Per questo scopo, è stato utilizzato il metodo del disegno sperimentale della composizione centrale (CCD) per determinare i punti sperimentali. I dati di laboratorio sono stati quindi confrontati con l'output del modello, in modo da garantire una buona corrispondenza tra di loro. In seguito, l'ottimizzazione del processo è stata eseguita utilizzando il metodo RSM response procedure.",
"I risultati dello studio hanno mostrato che i valori ottimali delle variabili indipendenti, vale a dire il pH, COD, O3 e TiO2, sono 11, 200 mg/L, 5 g/h e 200 mg/L, rispettivamente. In queste condizioni, l'efficienza di rimozione del COD è stata del 96,3% in 50 minuti. Inoltre, è stato osservato che i cambiamenti nel livello di COD e l'input di ozono hanno un effetto significativo sull'efficienza complessiva di rimozione del COD. I risultati hanno anche dimostrato che un aumento del livello di COD e dell'input di ozono aumenta l'efficienza di rimozione del COD. Tuttavia, un aumento del livello di catalizzatore non ha avuto alcun effetto significativo sull'efficienza di rimozione del COD.",
"I risultati di questo studio hanno confermato che il metodo di ozonazione integrata/fotchimica può essere utilizzato con successo per trattare i rifiuti delle raffinerie e ridurre l'inquinamento organico. Tuttavia, i risultati hanno anche mostrato che l'efficienza del trattamento è fortemente dipendente dai livelli di COD e dall'input di ozono. Quindi, per garantire un'elevata efficienza di trattamento, è necessario mantenere i livelli di COD e l'input di ozono entro i limiti ottimali.",
"In conclusione, questo studio ha mostrato che il metodo di ozonazione integrata/fotchimica è un metodo promettente per il trattamento dei rifiuti delle raffinerie e la riduzione dell'inquinamento organico. I risultati hanno anche dimostrato che l'efficienza del trattamento è influenzata dall'importo iniziale di COD e dall'input di ozono. Pertanto, è necessario mantenere i livelli di COD e l'input di ozono entro i limiti ottimali per garantire un'elevata efficienza di trattamento. Inoltre, è importante sottolineare che i dati ottenuti in questo studio sono derivati da esperimenti di laboratorio e devono essere confermati con ulteriori ricerche su scala più ampia. Infine, il metodo utilizzato in questo studio potrebbe essere utilizzato anche per il trattamento di altri tipi di effluenti industriali con una contaminazione organica simile.",
            ]
            paragraph = paragraphs[paragraph_index]
            prompt = f'''
                Espandi di poco il seguente paragrafo: {paragraph}
            '''
            reply = util_ai.gen_reply(prompt).strip()
            if reply != '':
                print('*********************************************************')
                print(reply)
                print('*********************************************************')
                data[key][paragraph_index] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.SLEEP_TIME)
            paragraph_index += 1
        else:
            break

    body_to_draw = [item for item in data['body_large']]
    body_small = data['body_small'].split('\n')
    # print(len(body_to_draw))
    # print(len(body_small))
    # quit()
    for i in range(len(body_to_draw)-1, 0, -1):
        print(i)
        if body_to_draw[i] != body_small[i]:
            body_to_draw[i] = body_small[i]
            break

    text = ''
    for paragraph in body_to_draw:
        text += paragraph
    text = text.replace('\n', ' ').strip()
    mag.a4_draw_text_study(draw, text, grid_map, commit=True)


    print(is_under)
    

    export_url = data['export_url']
    img.save(export_url)

    quit()
