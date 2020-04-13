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


def get_recommendation(weather_info):
    """
    :param weather_info: information about current weather
    :return: recommendation what you need to wear if you want to go outside
    """
    pass

