import os
import sys
import buttons_holding
import pygame
import alphabets
import get_api
import gui


pygame.init()
wight, height = 600, 560
screen = pygame.display.set_mode((wight, height))
buttons_holding.init()
gui.init()

language = 'eng'
shift = False
pt = None
alphs = {'rus': alphabets.alphabet_rus, 'eng': alphabets.alphabet_eng}
postal_code = ''


def nor(b1: bool, b2: bool):
    return (b1 or b2) and not(b1 and b2)


def toggle(b: bool):
    return not b


def toggle_postal():
    gui.toggle_button('bool_postal')
    if gui.buttons['bool_postal'].active:
        gui.buttons['postal_code'].text = postal_code
    else:
        gui.buttons['postal_code'].text = ''


def change_text(key):
    if key == pygame.K_BACKSPACE:
        if gui.buttons['word_in'].text != '':
            gui.buttons['word_in'].text = gui.buttons['word_in'].text[:-1]
    if len(gui.buttons['word_in'].text) < 30:
        try:
            if shift:
                text = gui.buttons['word_in'].text + alphs[language][key].upper()
            else:
                text = gui.buttons['word_in'].text + alphs[language][key]
            gui.buttons['word_in'].text = text
        except BaseException:
            return None


def reset_pt():
    global pt, postal_code
    gui.buttons['address'].text = ''
    postal_code = ''
    gui.buttons['postal_code'].text = ''
    pt = None
    load_image(map_type)


def change_map_type(type1):
    global map_type
    gui.select_button('plan', False)
    gui.select_button('sputnik', False)
    gui.select_button('hybrid', False)
    map_type = type1
    d = {'map': 'plan', 'sat': 'sputnik', 'sat,skl': 'hybrid'}
    gui.select_button(d[type1], True)
    load_image(map_type)


def search():
    if gui.buttons['word_in'].text != '':
        response = get_api.search(gui.buttons['word_in'].text)
        if response:
            try:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                    "GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                gui.buttons['address'].text = toponym_address
                global pt, cords
                cords = list(map(float, toponym_coodrinates.split()))
                pt = ','.join(toponym_coodrinates.split()) + ',' + 'org'
                load_image(map_type)
            except BaseException:
                return None
            try:
                global postal_code
                toponym_postal_code = toponym["metaDataProperty"]["GeocoderMetaData"][
                    "Address"]['postal_code']
                postal_code = toponym_postal_code
                if gui.buttons['bool_postal'].active:
                    gui.buttons['postal_code'].text = postal_code
            except BaseException:
                postal_code = ''
                return None


def change_zoom(n):
    global zoom
    zoom += n
    if zoom > 17:
        zoom = 17
    elif zoom < 0:
        zoom = 0
    load_image(map_type)


def load_image(map_type='map'):
    response = get_api.get_map(",".join(map(str, cords)), str(zoom), map_type, pt)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


def move_map(cord, znac):
    cords[cord] += 10 * (0.1 ** (zoom // 2 - 2)) * znac
    if cord == 1:
        if cords[1] > 85:
            cords[1] = 85
        elif cords[1] < -85:
            cords[1] = -85
    else:
        cords[0] = (cords[0] + 180) % 360 - 180
    load_image(map_type)


cords = [37.622504, 55.753215]
zoom = 15
map_file = "map.png"
map_type = 'map'
load_image()
running = True
buttons_holding.add_button(pygame.K_UP, move_map, 1, 1)
buttons_holding.add_button(pygame.K_DOWN, move_map, 1, -1)
buttons_holding.add_button(pygame.K_RIGHT, move_map, 0, 1)
buttons_holding.add_button(pygame.K_LEFT, move_map, 0, -1)
buttons_holding.add_button(pygame.K_PAGEUP, change_zoom, 1)
buttons_holding.add_button(pygame.K_PAGEDOWN, change_zoom, -1)

gui.add_button('plan', False, 0, 0, 70, 30, 'Схема', 25, (127, 127, 127), (191, 191, 191),
               (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'map')
gui.select_button('plan', True)
gui.add_button('sputnik', False, 0, 30, 70, 30, 'Спутник', 25, (127, 127, 127), (191, 191, 191),
               (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'sat')
gui.add_button('hybrid', False, 0, 60, 70, 30, 'Гибрид', 25, (127, 127, 127), (191, 191, 191),
               (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'sat,skl')
gui.add_button('word_in', True, 0, height - 90, wight, 30, '', 25, (159, 159, 159),
               (191, 191, 191), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_text)
gui.add_button('search', False, wight - 80, height - 120, 80, 30, 'Найти', 25, (127, 127, 127),
               (191, 191, 191), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), search)
gui.add_button('reset_pt', False, 0, height - 120, wight - 80, 30, 'Сброс поискового результата',
               25, (127, 127, 127), (191, 191, 191), (255, 255, 255),
               (0, 0, 0), (0, 0, 0), (0, 0, 0), reset_pt)
gui.add_button('address', False, 0, height - 60, wight, 30, '', 25, (127, 127, 127),
               (127, 127, 127), (127, 127, 127), (0, 0, 0), (0, 0, 0), (0, 0, 0), int)
gui.add_button('bool_postal', False, 0, height - 30, 200, 30, 'Индекс', 25, (127, 0, 0),
               (127, 0, 0), (0, 127, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), toggle_postal)
gui.add_button('postal_code', False, 200, height - 30, wight - 200, 30, '', 25, (127, 127, 127),
               (127, 127, 127), (127, 127, 127), (0, 0, 0), (0, 0, 0), (0, 0, 0), int)
mouse_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.mod and (pygame.KMOD_ALT and event.key == pygame.K_LSHIFT or
                              pygame.KMOD_SHIFT and event.key == pygame.K_LALT):
                if language == 'eng':
                    language = 'rus'
                else:
                    language = 'eng'
            if event.key == pygame.K_LSHIFT:
                shift = True
            else:
                buttons_holding.activate_button(event.key, True)
                gui.button_key_actions(event.key)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                shift = False
            else:
                buttons_holding.activate_button(event.key, False)
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            gui.button_clicked(event.pos)
    buttons_holding.buttons_actions()
    gui.draw_buttons(screen, mouse_pos)
    pygame.display.flip()
pygame.quit()
os.remove(map_file)