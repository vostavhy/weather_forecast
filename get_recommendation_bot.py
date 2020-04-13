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


def get_recommendation(weather_info):
    """
    :param weather_info: information about current weather
    :return: recommendation what you need to wear you want to go outside
    """
    pass


def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT + '')


def help(update, context):
    """Send a message when the command /help is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_HELP)


def info(update, context):
    """Send a message with info about the weather when city is typed"""
    city = context.args[0]

    # get weather info from weather api
    weather_info = get_weather_info(city=city, OPEN_WEATHER_TOKEN)

    # get weather recommendations
    recommendation = get_recommendation(weather_info=weather_info)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Погода в городе {city}: \n {weather_info}'
                                                                    f'Рекомендации по одежде: {recommendation}')


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
    echo_handler = MessageHandler(Filters.text, info)

    # in case of unknown command
    unknown_handler = MessageHandler(Filters.command, unknown)

    # register our commands in dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_error_handler(error)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()
