import pygame


buttons = {}


class Button:
    def __init__(self, x, y, d_x, d_y, text, size, bc_nonact, bc_sel, bc_act,
                 tc_nonact, tc_sel, tc_act, f, *args, **kwargs):
        self.active = False
        self.x = x
        self.y = y
        self.d_x = d_x
        self.d_y = d_y
        self.text = text
        self.size = size
        self.bc_nonact = bc_nonact
        self.bc_sel = bc_sel
        self.bc_act = bc_act
        self.tc_nonact = tc_nonact
        self.tc_sel = tc_sel
        self.tc_act = tc_act
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def get_centre(self):
        return self.x + int(self.d_x / 2), self.y + int(self.d_y / 2)

    def check_selection(self, pos):
        return 0 <= pos[0] - self.x <= self.d_x and 0 <= pos[1] - self.y <= self.d_y

    def select(self, b: bool):
        self.active = b


def init():
    global buttons
    pygame.init()
    buttons = {}


def draw_rect_const(screen, color, x1, y1, x2, y2, wide=0):
    pygame.draw.rect(screen, color, (x1, y1, x2 - x1, y2 - y1), wide)


def draw_rect(screen, color, x, y, d_x, d_y, wide1=0):
    pygame.draw.rect(screen, color, (x, y, d_x, d_y), wide1)


def draw_text_at_corner(screen, color, text, x, y, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    screen.blit(text, (x, y))


def draw_text_at_centre(screen, color, text, x, y, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


def add_button(id, x, y, d_x, d_y, text, size, bc_nonact, bc_sel, bc_act,
               tc_nonact, tc_sel, tc_act, f, *args, **kwargs):
    buttons[id] = Button(x, y, d_x, d_y, text, size, bc_nonact, bc_sel, bc_act,
                         tc_nonact, tc_sel, tc_act, f, *args, **kwargs)


def draw_buttons(screen, pos=None):
    for key, item in buttons.items():
        if item.active:
            draw_rect(screen, item.bc_act, item.x, item.y, item.d_x, item.d_y)
            draw_text_at_centre(screen, item.tc_act, item.text, *item.get_centre(), item.size)
        elif item.check_selection(pos):
            draw_rect(screen, item.bc_sel, item.x, item.y, item.d_x, item.d_y)
            draw_text_at_centre(screen, item.tc_sel, item.text, *item.get_centre(), item.size)
        else:
            draw_rect(screen, item.bc_nonact, item.x, item.y, item.d_x, item.d_y)
            draw_text_at_centre(screen, item.tc_nonact, item.text, *item.get_centre(), item.size)


def button_clicked(pos):
    for key, item in buttons.items():
        if item.check_selection(pos):
            item.f(*item.args, **item.kwargs)


def select_button(id, b: bool):
    buttons[id].select(b)