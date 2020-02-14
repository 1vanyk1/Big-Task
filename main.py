import os
import sys
import buttons_holding
import pygame
import requests
import get_api
import gui


pygame.init()
screen = pygame.display.set_mode((600, 450))
buttons_holding.init()
gui.init()


def change_map_type(type1):
    global map_type
    gui.select_button('plan', False)
    gui.select_button('sputnik', False)
    gui.select_button('hybrid', False)
    map_type = type1
    d = {'map': 'plan', 'sat': 'sputnik', 'sat,skl': 'hybrid'}
    gui.select_button(d[type1], True)
    load_image(map_type)


def change_zoom(n):
    global zoom
    zoom += n
    if zoom > 17:
        zoom = 17
    elif zoom < 0:
        zoom = 0
    load_image(map_type)


def load_image(map_type='map'):
    map_request = get_api.get_map(",".join(map(str, cords)), str(zoom), map_type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
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

gui.add_button('plan', 0, 0, 70, 30, 'Схема', 25, (127, 127, 127), (191, 191, 191), (255, 255, 255),
               (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'map')
gui.select_button('plan', True)
gui.add_button('sputnik', 0, 30, 70, 30, 'Спутник', 25, (127, 127, 127), (191, 191, 191),
               (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'sat')
gui.add_button('hybrid', 0, 60, 70, 30, 'Гибрид', 25, (127, 127, 127), (191, 191, 191),
               (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), change_map_type, 'sat,skl')
mouse_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            buttons_holding.activate_button(event.key, True)
        if event.type == pygame.KEYUP:
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