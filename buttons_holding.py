buttons = {}
buttons_act = {}
args_act = {}
kwargs_act = {}


def init():
    global buttons_act, buttons
    buttons = {}
    buttons_act = {}


def buttons_actions():
    for i in buttons.keys():
        if buttons[i]:
            buttons_act[i](*args_act[i], **kwargs_act[i])


def activate_button(button, b: bool):
    if button in buttons.keys():
        buttons[button] = b


def add_button(button, f, *args, **kwargs):
    buttons[button] = False
    buttons_act[button] = f
    args_act[button] = args
    kwargs_act[button] = kwargs