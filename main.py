import os
import sys

import pygame
import requests
import get_api


# geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
# geocoder_params = {
#     "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
#     "geocode": "37.622504,55.753215",
#     "format": "json"}
# response = requests.get(geocoder_api_server, params=geocoder_params)
# json_response = response.json()
# toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# toponym_coodrinates = ','.join(toponym["Point"]["pos"].split())
# corners = [list(map(float, i.split())) for i in toponym['boundedBy']['Envelope'].values()]
# corners = ','.join([str(corners[1][0] - corners[0][0]), str(corners[1][1] - corners[0][1])])
# response = None
cords = [37.622504, 55.753215]
zoom = 0.01
map_request = get_api.get_map(",".join(map(str, cords)), str(zoom) + ',' + str(zoom))
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)