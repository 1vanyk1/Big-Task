import requests


def get_map(toponym_coodrinates, corners, map_type='sat', pt=None):
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {"ll": toponym_coodrinates,
              "z": corners,
              "l": map_type,
              'size': '600,450'}
    if pt is not None:
        params['pt'] = pt
    request = requests.get(api_server, params=params)
    return request


def search(geocode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json"}
    return requests.get(geocoder_api_server, params=geocoder_params)