import g

def a4_draw_grid(draw):
    for i in range(g.GRID_COL_NUM+1):
        x_1 = int(g.CELL_SIZE*10/2*i)
        y_1 = 0
        x_2 = int(g.CELL_SIZE*10/2*i)
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)

    for i in range(g.GRID_ROW_NUM+1):
        x_1 = 0
        y_1 = int(g.CELL_SIZE*10/2*i)
        x_2 = g.A4_WIDTH
        y_2 = int(g.CELL_SIZE*10/2*i)
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GRID, width=4)


def a4_draw_guides(draw, guide_size):
    for i in range(g.GRID_COL_NUM+1):
        x_1 = int(guide_size*10/2*i)
        y_1 = 0
        x_2 = int(guide_size*10/2*i)
        y_2 = g.A4_HEIGHT
        draw.line((x_1, y_1, x_2, y_2), fill=g.C_GUIDE, width=8)

