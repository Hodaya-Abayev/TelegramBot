
#!/usr/bin/env python
# -- coding: utf-8 --
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telebot
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bs4 import BeautifulSoup as bs
#import pandas as pd
#pd.set_option('display.max_colwidth', 500)
import time
import requests
import random

engine = create_engine('sqlite:///my-sqlite1.db', echo=True)

Base = declarative_base()
session_maker = sessionmaker(bind=engine)


class CovidTestingPositions(Base):
    """
    Database for storing the places of corona testing
    """
    __tablename__: str = 'covid_testing_positions'
    area = Column(String)
    city = Column(String, primary_key=True)

def get_session():
    return session_maker()


def initialize_data_base():
    page = requests.get(
        "https://www.leumit.co.il/heb/Life/FamilyHealth/familyhealth/coronavirus/CoronaTesting1/articlegalleryitem,3967/")
    soup = bs(page.content, features="html.parser")
    table = soup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')

    for row in rows:
        #print(row.contents[1].get_text(strip=True),row.contents[3].get_text(strip=True))
        new_row = CovidTestingPositions(area=row.contents[1].get_text(strip=True),city=row.contents[3].get_text(strip=True))
        session = get_session()
        session.add(new_row)
        session.commit()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def import_data_from_api():
    page = requests.get("https://corona.mako.co.il/")
    return bs(page.content, features='html.parser')



def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text('היי '+first_name+'!'+'\n'+'אני בוט שנותן מידע על מצב הקורונה ועל עמדות בדיקות בארץ.'+'\n'+'אני מתעדכן כל הזמן וכך מתקבל מידע בזמן אמת.'+
                              '\n'+'אני עדיין בשלבי פיתוח ואני משתפר מיום ליום:)'+'\n\n'+'אשמח לעמוד לשירותך!')
    menu(update, context)


def menu(update, context):
    buttons = [
        ['/A'],['/B']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    update.message.reply_text('בחר/י אחת מהאפשרויות הבאות:'+'\n'+'תמונות מצב כלליות על הקורונה בארץ (/A)'+'\n'+  'מידע על מתחמי מדיקות קורונה ברחבי הארץ (/B)'+'\n', reply_markup=keyboard)





def testing_positions(update, context):
    pos=[]
    """return list of testing positions according to the area"""
    for i in get_session().query(CovidTestingPositions.city, CovidTestingPositions.area):
        pos.append((i[0], i[1]))
    index=update.message.text[1]
    if index=='N':
        positions= list(filter(lambda p: p[1]=='צפון', pos))
    elif index=='S':
        positions = list(filter(lambda p: p[1] == 'דרום', pos))
    elif index=='C':
        positions = list(filter(lambda p: p[1] == 'מרכז', pos))
    elif index=='J':
        positions = list(filter(lambda p: p[1] == 'ירושלים', pos))
    reply='\n'.join(i[0] for i in positions)
    update.message.reply_text(reply+'\n')

def get_covid_info(update, context):
    covid_data = import_data_from_api()
    index = int(update.message.text[1])
    if index == 1:
        desc = " מספר החולים קשה: "
    if index == 2:
        desc = " מספר המאושפזים: "
    if index == 3:
        desc = " מספר המתחסנים במנה שניה: "
    if index == 4:
        desc = " אחוז בדיקות חיוביות: "
    ans = get_morbidity_status(covid_data)[index-1].get_text()
    update.message.reply_text(desc + ans)


def get_morbidity_status(data):
    return data.find_all(class_="stat-total")



def covid_info(update, context):
    buttons = [
        ['/1'],['/2'],['/3'], ['/4'],['/menu']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('מה תרצה/י לדעת?')
    update.message.reply_text('מספר חולים קשה (/1)'+'\n'+'מספר מאושפזים (/2)'+'\n'+'מספר המחוסנים במנה שניה (/3)'+'\n'+'אחוז בדיקות חיוביות (/4)' +'\n',reply_markup=keyboard)


def get_testing_positions(update, context):
    buttons = [
        ['/N'], ['/S'], ['/C'], ['/J'], ['/menu']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('באיזה אזור תרצה לבצע בדיקה?')
    update.message.reply_text('צפון (/N)'+'\n'+'דרום (/S)'+'\n'+'מרכז (/C)'+'\n'+'ירושלים (/J)'+'\n', reply_markup=keyboard)



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__=="__main__":
    #Base.metadata.create_all(engine)
    #initialize_data_base()
    print("hi")



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
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler('N', testing_positions))
    dp.add_handler(CommandHandler('S', testing_positions))
    dp.add_handler(CommandHandler('C', testing_positions))
    dp.add_handler(CommandHandler('J', testing_positions))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(RegexHandler("tests", testing_positions))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()









