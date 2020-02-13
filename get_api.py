def get_map(toponym_coodrinates, corners, map_type='sat'):
    return "http://static-maps.yandex.ru/1.x/?ll=" + toponym_coodrinates + "&z=" + corners + "&l=" + map_type