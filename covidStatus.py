import requests
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup as bs

def import_data_from_api():
    """

    :return: data of the covid status in israel from the API
    """
    page = requests.get("https://corona.mako.co.il/")
    return bs(page.content, features='html.parser')


def covid_info(update, context):
    buttons = [
        ['/1'],['/2'],['/3'], ['/4'],['/menu']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('מה תרצה/י לדעת?')
    update.message.reply_text('מספר חולים קשה (/1)'+'\n'+'מספר מאושפזים (/2)'+'\n'+'מספר המחוסנים במנה שניה (/3)'+'\n'+'אחוז בדיקות חיוביות (/4)' +'\n',reply_markup=keyboard)

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

