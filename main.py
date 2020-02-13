import os
import sys

import pygame
import requests
import get_api


pygame.init()
screen = pygame.display.set_mode((600, 450))


def load_image():
    map_request = get_api.get_map(",".join(map(str, cords)), str(zoom), 'map')
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


cords = [37.622504, 55.753215]
zoom = 15
map_file = "map.png"
load_image()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                if zoom < 17:
                    zoom += 1
                load_image()
            elif event.key == pygame.K_PAGEDOWN:
                if zoom > 0:
                    zoom -= 1
                load_image()
    pygame.display.flip()
pygame.quit()
os.remove(map_file)