
#!/usr/bin/env python
# -- coding: utf-8 --
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Include.covidStatus import get_covid_info, covid_info
from Include.flights import get_country, get_country_info
from Include.positionsDataBase import get_testing_positions, testing_positions






# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.




def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text('היי '+first_name+'!'+'\n'+'אם את/ה רוצה לטוס לחו"ל, ולא יודע מה מצב הקורונה ביעד, הגעת למקום הנכון!'+'\n\n'+'אני בוט שנותן מידע על מצב הקורונה בארץ ובעולם, ובמידה והינך נדרש/ת בדיקה לפני הטיסה, תוכל למצוא את מתחמי בדיקות הקורונה הקרובים אליך.'+'\n\n'+'אני מתעדכן כל הזמן וכך מתקבל מידע בזמן אמת.'+
                              '\n'+'אני עדיין בשלבי פיתוח ואני משתפר מיום ליום:)'+'\n\n'+'אשמח לעמוד לשירותך!')
    menu(update, context)


def menu(update, context):
    buttons = [
        ['/A'],['/B'],['/C']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('בחר/י אחת מהאפשרויות הבאות:'+'\n'+'תמונות מצב כלליות על הקורונה בארץ (/A)'+'\n'+  'מידע על מתחמי בדיקות קורונה ברחבי הארץ (/B)'+'\n'
                              +'מידע על הגבלות הכניסה והתיירות ביעד אליו תרצה/י לטוס (/C)', reply_markup=keyboard)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__=="__main__":
    #Base.metadata.create_all(engine)
    #initialize_data_base()


    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1971668904:AAG_DS4EgEXGmR7pJ84pmuo7xTTSP9WlRdI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("1", get_covid_info))
    dp.add_handler(CommandHandler("2", get_covid_info))
    dp.add_handler(CommandHandler("3", get_covid_info))
    dp.add_handler(CommandHandler("4", get_covid_info))
    dp.add_handler(CommandHandler("A", covid_info))
    dp.add_handler(CommandHandler("B", get_testing_positions))
    dp.add_handler(CommandHandler("C", get_country))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler('NORTH', testing_positions))
    dp.add_handler(CommandHandler('SOUTH', testing_positions))
    dp.add_handler(CommandHandler('CENTER', testing_positions))
    dp.add_handler(CommandHandler('JERUSALEM', testing_positions))
    dp.add_handler(MessageHandler(Filters.text, get_country_info))

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()









