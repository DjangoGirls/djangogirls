import requests

def get_coordinates_for_city(city, country):

    req = requests.get('http://nominatim.openstreetmap.org/search', params={'format': 'json', 'q': '{0}, {1}'.format(city.encode('utf-8'), country.encode('utf-8'))})

    try:
        data = req.json()[0]
        return '{0}, {1}'.format(data['lat'], data['lon'])
    except IndexError:
        return None
