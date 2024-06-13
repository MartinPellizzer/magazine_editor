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
