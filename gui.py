import pygame


buttons = {}


def init():
    global buttons
    pygame.init()
    buttons = {}


def draw_rect_const(screen, color, x1, y1, x2, y2, wide=0):
    pygame.draw(screen, color, (x1, y1, x2 - x1, y2 - y1), wide)


def draw_rect(screen, color, x, y, d_x, d_y, wide1=0):
    print(screen, color, x, y, d_x, d_y, wide1)
    pygame.draw(screen, color, (x, y, d_x, d_y), wide1)


def draw_text_at_corner(screen, color, text, x, y, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    screen.blit(text, (x, y))


def draw_text_at_centre(screen, color, text, x, y, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


def add_button(id, x, y, d_x, d_y, text, size, bc_nonact, bc_sel, bc_act, tc_nonact, tc_sel, tc_act):
    buttons[id] = {'active': False, 'x': x, 'y': y, 'd_x': d_x, 'd_y': d_y, 'text': text, 'size': size,
                   'bc_nonact': bc_nonact, 'bc_sel': bc_sel, 'bc_act': bc_act, 
                   'tc_nonact': tc_nonact, 'tc_sel': tc_sel, 'tc_act': tc_act}


def draw_buttons(screen, pos=None):
    for key, item in buttons.items():
        draw_rect(screen, item['bc_nonact'], item['x'], item['y'], item['d_x'], item['d_y'])
        draw_text_at_centre(screen, item['tc_nonact'], item['text'], item['x'], item['y'], item['size'])