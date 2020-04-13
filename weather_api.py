import requests

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?lang=ru&units=metric'


def get_weather_info(city, token):
    params = {
        'q': city,
        'APPID': token,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
