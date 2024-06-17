SLEEP_TIME = 30

C_GRID = '#cdcdcd'
C_GUIDE = '#ff00ff'


with open('demo_article.txt', 'r', encoding='utf-8', errors='ignore') as f: 
    DEMO_TEXT = f.read().replace('\n', ' ')

with open('placeholder_text.txt', 'r', encoding='utf-8', errors='ignore') as f: 
    PLACEHOLDER_TEXT = f.read().replace('\n', ' ')



BODY_FONT_SIZE = 30
TITLE_FONT_SIZE = 200

A4_WIDTH = 2480
A4_HEIGHT = 3508
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
PAGE_WIDTH = int(A4_WIDTH/10*2)
PAGE_HEIGHT = int(A4_HEIGHT/10*2)

GRID_CELL_SIZE = 16
GRID_COL_NUM = int(PAGE_WIDTH / GRID_CELL_SIZE)
GRID_ROW_NUM = int(PAGE_HEIGHT / GRID_CELL_SIZE) + 1

A4_CELL_SIZE = int(GRID_CELL_SIZE*10/2)

C_IMAGES = [
    '#41EAD4',
    '#FF9F1C',
    '#2A1E5C',
    '#55286F',
    '#8EA604',
    '#FF4E00',
    '#2AB7CA',
    '#717C89',
    '#ADF6B1',
    '#223127',
    '#CE5374',
]