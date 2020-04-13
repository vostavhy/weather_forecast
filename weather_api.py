import requests

BASE_URL = 'http://api.openweathermap.org/data/2.5/'


def get_weather_info(city, token):
    url_current = BASE_URL + '/weather'
    url_forecast = BASE_URL + '/forecast'
    params = {
        'q': city,
        'APPID': token,
        'lang': 'ru',
        'units': 'metric'
    }

    # get current weather
    response_current = requests.get(url=url_current, params=params)
    response_current.raise_for_status()

    # get forecast
    response_forecast = requests.get(url=url_forecast, params=params)
    response_forecast.raise_for_status()

    return response_current.json(), response_forecast.json()
