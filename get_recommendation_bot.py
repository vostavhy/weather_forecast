import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from weather_api import get_weather_info
import logging

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN')

TEXT = 'Привет! Я помогу Вам узнать погоду в любом городе. Просто напишите название города, например: Москва \n' \
       'или /help для помощи'

TEXT_HELP = 'Для того, чтобы узнать погоду в городе и получить рекомендации по одежде, напишите название города. ' \
            'Например: "Москва" (без кавычек) - если хотите узнать погоду в Москве'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_recommendation(temp, is_rain):
    """
    :param temp: information about current temperature
    :param is_rain: True if rainy and False if not
    :return: recommendation what you need to wear if you want to go outside
    """
    temp = int(temp)

    temp_status = {
        'очень жарко': 'хватит плавок и обязательно одень кепку',
        'жарко': 'достаточно одеть шорты, майку и шлепки',
        'прохладно': 'можно одеть ветровку, легкие штаны и кросовки',
        'холодно': 'советую одеть теплую куртку, плотные штаны и ботинки с толстой подошвой',
        'очень холодно': 'настоятельно рекомендую одеть дубленку, утепленные штаны, шапку, варешки и зимнюю обувь'
    }

    # get status regarding the current temperature
    if temp > 35:
        status = 'очень жарко'
    elif 22 < temp <= 35:
        status = 'жарко'
    elif 10 < temp <= 22:
        status = 'прохладно'
    elif -10 < temp <= 10:
        status = 'холодно'
    else:
        status = 'очень холодно'

    recommendation = f'Рекоммендация по одежде:\n' \
                     f'Так как на улице {status}, {temp_status.get(status)}.'
    if is_rain:
        recommendation += 'Также на улице идет дождь, захвати с собой зонт.'

    return recommendation


def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT + '')


def help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_HELP)


def info(update, context):
    """Send a message with info about the weather when city is typed"""
    city = update.message.text
    my_message = ''

    try:
        # get weather info from weather api
        weather_info = get_weather_info(city=city, token=OPEN_WEATHER_TOKEN)
        main_info = weather_info.get("main")
        description = weather_info.get("weather")[0].get("description")

        my_message += f'Погода в городе {city}: \n' \
                      f'{description} \n' \
                      f'температура: {main_info.get("temp")} °C \n' \
                      f'чувствуется как: {main_info.get("feels_like")} °C \n' \
                      f'давление: {main_info.get("pressure")} Па \n' \
                      f'влажность: {main_info.get("humidity")} % \n' \
                      f'скорость ветра: {weather_info.get("wind").get("speed")} м/с \n\n' \

        recommendation = get_recommendation(main_info.get('feels_like'), description == 'дождь')

        my_message += recommendation

    except Exception as e:
        logger.warning(f'Бот упал с ошибкой: {e}')
        my_message += f'К сожалению, у меня нет информации для города {city}. Проверьте правильность названия города.'

    # get weather recommendations
    # recommendation = get_recommendation(weather_info=weather_info)

    context.bot.send_message(chat_id=update.effective_chat.id, text=my_message)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, но данная команда мне неизвестна \n')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    """Start the bot"""
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # commands
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    # on text message bot should return info about the weather
    info_handler = MessageHandler(Filters.text, info)

    # in case of unknown command
    unknown_handler = MessageHandler(Filters.command, unknown)

    # register our commands in dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_error_handler(error)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()
