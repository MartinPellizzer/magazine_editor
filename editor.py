import os

import pygame
from PIL import Image, ImageDraw, ImageFont

import util

A4_WIDTH = 2480 * 2
A4_HEIGHT = 3508


WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

CANVAS_WIDTH = A4_WIDTH//4
CANVAS_HEIGHT = A4_HEIGHT//4

canvas_x = WINDOW_WIDTH//2 - CANVAS_WIDTH//2
canvas_y = WINDOW_HEIGHT//2 - CANVAS_HEIGHT//2

cols_num = 64
rows_num = int(cols_num*1.41/2)

a4_col_w = A4_WIDTH / cols_num
a4_row_h = A4_HEIGHT / rows_num
print(a4_col_w)
print(a4_row_h)

col_width = CANVAS_WIDTH / cols_num
row_height = CANVAS_HEIGHT / rows_num
cols_gap = col_width//4

p1_margin_left = col_width*3
p1_margin_right = col_width*5

p2_margin_left = col_width*5
p2_margin_right = col_width*3

print_area_w = CANVAS_WIDTH//2 - p1_margin_left - p1_margin_right

grid_map = []
for row_i in range(rows_num):
    row_curr = []
    for col_i in range(cols_num):
        row_curr.append('')
    grid_map.append(row_curr)


######################################################################################################
# MAGAZINE 
######################################################################################################
def magazine_img(img, draw, i):
    start_col_i = -1
    start_row_i = -1
    end_col_i = -1
    end_row_i = -1
    for row_i in range(rows_num):
        for col_i in range(cols_num):
            if f'i_{i}' in tmp_grid_map[row_i][col_i]:
                if start_col_i == -1: start_col_i = col_i
                if start_row_i == -1: start_row_i = row_i
                end_col_i = col_i
                end_row_i = row_i
    end_row_i += 1
    end_col_i += 1
    if start_col_i != -1 and start_row_i != -1 and end_col_i != -1 and end_col_i != -1: 
        x = int(start_col_i*a4_col_w)
        y = int(start_row_i*a4_row_h)
        w = int(end_col_i*a4_col_w) - x
        h = int(end_row_i*a4_row_h) - y
        print(x, y, w, h)
        foreground = Image.open('image-test.png')
        util.img_resize_save(
            'image-test.png', 'image-test-resized.jpg', 
            w=w, h=h, 
            quality=100,
        )
        foreground = Image.open('image-test-resized.jpg')
        img.paste(foreground, (x, y))
    return img

def magazine_body(draw, text):
    body_font_size = 30
    body_font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", body_font_size)
    text = text.replace('\n', '').strip()

    done_grid_map = []
    for row_i in range(rows_num):
        row_curr = []
        for col_i in range(cols_num):
            row_curr.append('')
        done_grid_map.append(row_curr)
        
    lines_coord = []
    for col_i in range(cols_num):
        for row_i in range(rows_num):
            if 'b' in grid_map[row_i][col_i]:
                if done_grid_map[row_i][col_i] != 'b':
                    done_grid_map[row_i][col_i] = 'b'
                    tmp_line_coord = []
                    for next_col_i in range(col_i, cols_num):
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
            if line_curr_w + word_w < (line_coord[3] - line_coord[1]) * a4_col_w:
                line_curr += f'{word} '
            else:
                lines.append(line_curr.strip())
                line_curr = f'{word} '
            if len(lines) >= 2: break
        lines.append(line_curr.strip())

        x_1 = a4_col_w * line_coord[1]
        y_1 = a4_row_h * line_coord[0]

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
                if len(words) - 1 != 0:
                    space_length = (((line_coord[3] - line_coord[1]) * a4_col_w) - words_length) / (len(words) - 1)
                else: 
                    space_length = 0
                x = x_1
                for word in words:
                    draw.text((x, y_1 + (body_font_size * 1.3 * i)), word, font=body_font, fill=c_body)
                    x += draw.textlength(word, font=body_font) + space_length
            else:
                draw.text((x_1, y_1 + (body_font_size * 1.3 * i)), line, c_body, font=body_font)
                break

        if is_last_line: break

def magazine_title(draw, title):
    font_text = 'assets/fonts/helvetica/Helvetica-Bold.ttf'
    col_i_1 = -1
    row_i_1 = -1
    col_i_2 = -1
    row_i_2 = -1
    for row_i in range(rows_num):
        for col_i in range(cols_num):
            if 't' in grid_map[row_i][col_i]:
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i

    title_available_w = (col_i_2 - col_i_1 + 1) * a4_col_w
    title_available_h = (row_i_2 - row_i_1 + 1) * a4_row_h

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
        x_1 = a4_col_w * col_i_1
        y_1 = a4_row_h * row_i_1
        draw.text((x_1, y_1), title, text_color, font=title_font)



def magazine_title_constrained_y_new(draw, title):
    font_text = 'assets/fonts/helvetica/Helvetica-Bold.ttf'
    # GET TITLE BOX
    col_i_1 = -1
    row_i_1 = -1
    col_i_2 = -1
    row_i_2 = -1
    for row_i in range(rows_num):
        for col_i in range(cols_num):
            if 't' in grid_map[row_i][col_i]:
                if col_i_1 == -1 and row_i_1 == -1:
                    col_i_1 = col_i
                    row_i_1 = row_i
                else:
                    col_i_2 = col_i
                    row_i_2 = row_i
    
    x_1 = a4_col_w * col_i_1
    y_1 = a4_row_h * row_i_1
    x_2 = a4_col_w * (col_i_2 + 1)
    y_2 = a4_row_h * (row_i_2 + 1)
    
    title_available_w = x_2 - x_1
    title_available_h = y_2 - y_1

    title_color = '#000000'

    for i in range(32, 999):
        font_size = i
        title_font = ImageFont.truetype(font_text, font_size)
        words = title.split(' ')
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
        title_h = len(lines) * font_size
        if title_h > title_available_h: break


    for i, line in enumerate(lines):
        draw.text((x_1, y_1 + (font_size * i)), line, title_color, font=title_font)
    



def magazine_gen():
    img = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    for i in range(10):
        img = magazine_img(img, draw, i)
    with open('body-test.txt') as f: text = f.read()
    magazine_body(draw, text)
    title_text = "L'efficacia dell'ozonizzazione con microbolle nell'eliminare l'atrazina dalle fonti di acqua naturale"
    # magazine_title(draw, title_text)
    magazine_title_constrained_y_new(draw, title_text)
    img.show()



######################################################################################################
# PYGAME 
######################################################################################################

body_font_size = 14

pygame.init()
pygame.display.set_caption("Magazine Editor")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
my_font = pygame.font.SysFont('./assets/fonts/arial/ARIAL.TTF', 14)

grid_show = True

util.img_resize_save('image-test.png', 'image-test-resized.jpg', w=CANVAS_WIDTH//2+col_width*3, h=CANVAS_HEIGHT, quality=100)
image_test = pygame.image.load('image-test-resized.jpg')

def grid_map_copy():
    tmp = []
    for row_i in range(rows_num):
        row_curr = []
        for col_i in range(cols_num):
            row_curr.append(grid_map[row_i][col_i])
        tmp.append(row_curr)
    return tmp

tmp_grid_map = grid_map_copy()

flag_brush_type = 'b'
flag_image_num = 0

drag_x_1 = -1
drag_y_1 = -1

flag_preview = True

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0: flag_image_num = 0
            if event.key == pygame.K_1: flag_image_num = 1
            if event.key == pygame.K_2: flag_image_num = 2
            if event.key == pygame.K_3: flag_image_num = 3
            if event.key == pygame.K_4: flag_image_num = 4
            if event.key == pygame.K_5: flag_image_num = 5
            if event.key == pygame.K_6: flag_image_num = 6
            if event.key == pygame.K_7: flag_image_num = 7
            if event.key == pygame.K_8: flag_image_num = 8
            if event.key == pygame.K_9: flag_image_num = 9

            if event.key == pygame.K_g:
                grid_show = not grid_show
            if event.key == pygame.K_SPACE:
                if flag_brush_type == 'i': flag_brush_type = 'b'
                elif flag_brush_type == 'b': flag_brush_type = 't'
                elif flag_brush_type == 't': flag_brush_type = 'i'
            if event.key == pygame.K_p:
                flag_preview = not flag_preview
            if event.key == pygame.K_o:
                 magazine_gen()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag_drag = True
            pos = pygame.mouse.get_pos()
            drag_x_1 = pos[0]
            drag_y_1 = pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            flag_drag = False
            grid_map = tmp_grid_map

        ## add blocks
        if pygame.mouse.get_pressed()[0]:
            tmp_grid_map = grid_map_copy()
            
            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - canvas_x) // col_width)
            drag_r_1 = int((drag_y_1 - canvas_y) // row_height)
            drag_c_2 = int((drag_x_2 - canvas_x) // col_width)
            drag_r_2 = int((drag_y_2 - canvas_y) // row_height)

            for row_i in range(rows_num):
                for col_i in range(cols_num):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):
                        
                        if flag_brush_type == 'i' and flag_image_num == 0:
                            if 'i_0' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_0'
                        if flag_brush_type == 'i' and flag_image_num == 1:
                            if 'i_1' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += f'i_1'
                        if flag_brush_type == 'b':
                            if 'b' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 'b'
                        if flag_brush_type == 't':
                            if 't' not in tmp_grid_map[row_i][col_i]:
                                tmp_grid_map[row_i][col_i] += 't'

        ## clear blocks
        if pygame.mouse.get_pressed()[2]:
            tmp_grid_map = grid_map_copy()

            pos = pygame.mouse.get_pos()
            drag_x_2 = pos[0]
            drag_y_2 = pos[1]

            drag_c_1 = int((drag_x_1 - canvas_x) // col_width)
            drag_r_1 = int((drag_y_1 - canvas_y) // row_height)
            drag_c_2 = int((drag_x_2 - canvas_x) // col_width)
            drag_r_2 = int((drag_y_2 - canvas_y) // row_height)

            for row_i in range(rows_num):
                for col_i in range(cols_num):
                    if (row_i >= drag_r_1 and row_i <= drag_r_2 and 
                        col_i >= drag_c_1 and col_i <= drag_c_2):

                        tmp_grid_map[row_i][col_i] = ''

    ## background
    pygame.draw.rect(screen, '#111111', (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    ## canvas
    pygame.draw.rect(screen, '#ffffff', (canvas_x, canvas_y, CANVAS_WIDTH, CANVAS_HEIGHT))

    ## image
    # if flag_preview:
    #    screen.blit(image_test, (canvas_x + CANVAS_WIDTH//2 - col_width*3, canvas_y))

    ## text
    '''
    with open('body-test.txt') as f: content = f.read()
    content = content.strip().replace('\n', ' ').replace('   ', ' ').replace('  ', ' ')
    lines = []
    line_curr = ''
    for word in content.split(' '):
        word_width, word_height = my_font.size(word)
        line_curr_width, line_curr_height = my_font.size(line_curr)
        if line_curr_width + word_width < col_width*3 - cols_gap:
            line_curr += f'{word} '
        else:
            lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr.strip())

    line_height_max = 0
    for line in lines:
        line_width, line_height = my_font.size(line)
        if line_height_max < line_height:
            line_height_max = line_height

    line_spacing = 1.2
    for line_i, line in enumerate(lines):
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#000000')
        line_x = canvas_x + col_width*1
        line_y = canvas_y + row_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - row_height*2:
            screen.blit(text_surface, (line_x, line_y))
    for line_i, line in enumerate(lines):
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#000000')
        line_x = canvas_x + col_width*4
        line_y = canvas_y + row_height*1 + (line_height_max*line_i*line_spacing)
        if line_y < canvas_y + CANVAS_HEIGHT - row_height*2:
            screen.blit(text_surface, (line_x, line_y))
    '''

    if grid_show:
        ## grid
        for i in range(cols_num+1):
            pygame.draw.line(screen, '#333333', (canvas_x + int(col_width*i), 0), (canvas_x + int(col_width*i), WINDOW_HEIGHT), 1)
        for i in range(rows_num+1):
            pygame.draw.line(screen, '#333333', (0, canvas_y + int(row_height*i)), (WINDOW_WIDTH, canvas_y + int(row_height*i)), 1)
        
    ## inner_cols
    inner_cols_num = 9
    inner_col_w = print_area_w / inner_cols_num

    for i in range(inner_cols_num+1):
        x1 = int(canvas_x + p1_margin_left + inner_col_w*i)
        y1 = int(canvas_y)
        x2 = int(canvas_x + p1_margin_left + inner_col_w*i)
        y2 = int(canvas_y + CANVAS_HEIGHT)
        pygame.draw.line(screen, '#00ffff', (x1, y1), (x2, y2), 2)
        
    for i in range(inner_cols_num+1):
        x1 = int(canvas_x + CANVAS_WIDTH//2 + p2_margin_left + inner_col_w*i)
        y1 = int(canvas_y)
        x2 = int(canvas_x + CANVAS_WIDTH//2 + p2_margin_left + inner_col_w*i)
        y2 = int(canvas_y + CANVAS_HEIGHT)
        pygame.draw.line(screen, '#00ffff', (x1, y1), (x2, y2), 2)

    ## guides
    # pygame.draw.line(screen, '#000000', (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT), 2)
    pygame.draw.line(screen, '#000000', (canvas_x + CANVAS_WIDTH//2, 0), (canvas_x + CANVAS_WIDTH//2, WINDOW_HEIGHT), 2)

    ## margins
    x1 = canvas_x + p1_margin_left
    y1 = canvas_y
    x2 = canvas_x + p1_margin_left
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)
    
    x1 = canvas_x + CANVAS_WIDTH//2 - p1_margin_right
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH//2 - p1_margin_right
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x + CANVAS_WIDTH//2 + p2_margin_left
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH//2 + p2_margin_left
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x + CANVAS_WIDTH - p2_margin_right
    y1 = canvas_y
    x2 = canvas_x + CANVAS_WIDTH - p2_margin_right
    y2 = canvas_y + CANVAS_HEIGHT
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x
    y1 = canvas_y + row_height*5
    x2 = canvas_x + CANVAS_WIDTH
    y2 = canvas_y + row_height*5
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    x1 = canvas_x
    y1 = canvas_y + CANVAS_HEIGHT - row_height*8
    x2 = canvas_x + CANVAS_WIDTH
    y2 = canvas_y + CANVAS_HEIGHT - row_height*8
    pygame.draw.line(screen, '#ff0000', (x1, y1), (x2, y2), 2)

    ## blocks colors
    for row_i in range(rows_num):
        for col_i in range(cols_num):
            if 'i_0' in tmp_grid_map[row_i][col_i]:
                red_x_1 = canvas_x + col_width * col_i
                red_y_1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#ff0000', (red_x_1, red_y_1, col_width, row_height))
            if 'i_1' in tmp_grid_map[row_i][col_i]:
                red_x_1 = canvas_x + col_width * col_i
                red_y_1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#ffff00', (red_x_1, red_y_1, col_width, row_height))
            
            if 'b' in tmp_grid_map[row_i][col_i]:
                x1 = canvas_x + col_width * col_i
                y1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#000000', (x1, y1, col_width, row_height))
            if 't' in tmp_grid_map[row_i][col_i]:
                x1 = canvas_x + col_width * col_i
                y1 = canvas_y + row_height * row_i
                pygame.draw.rect(screen, '#00ff00', (x1, y1, col_width, row_height))
           

    if 'debug':
        line_x = 0
        line_y = 0

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        line = f'x: {x} - y: {y}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16

        x = pos[0] - canvas_x
        y = pos[1] - canvas_y
        line = f'x: {x} - y: {y}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16
        
        col_i = int(x//col_width) 
        row_i = int(y//row_height)
        line = f'col_i: {col_i} - row_i: {row_i}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16
        
        line = f'flag_brush_type: {flag_brush_type}'
        line_width, line_height = my_font.size(line)
        text_surface = my_font.render(line, False, '#ff00ff')
        screen.blit(text_surface, (line_x, line_y))
        line_y += 16


    pygame.display.flip()
