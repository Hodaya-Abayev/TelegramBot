import requests
from bs4 import BeautifulSoup as bs
import json
from telegram import ReplyKeyboardMarkup


def get_country(update, context):
    update.message.reply_text("לאן תרצה/י לטוס?")


def import_flight_data_from_api():
    """
    get data for each country from the API
    :return:
    """
    page = requests.get("https://flightsinfo.mako.co.il/")
    flight= bs(page.content, features='html.parser')
    countries = flight.findAll(lambda tag: tag.name == 'script')[-2].string
    c=countries.split("=", 1)[1]
    return json.loads(c)["countries"]["data"]


def get_country_info(update, country):
    """
    :param update:
    :param country:
    :return: details for the wanted country
    """
    buttons = [['/menu']]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    for c in import_flight_data_from_api():
        if c["editorCountryName"]==update["message"]["text"]:
            information=[]
            # יעד פתוח או סגור
            if "closed" in c["entryRules"].keys():
                information.append(c["entryRules"]["closed"])
            else:
                information.append(c["entryRules"]["open"])
            # נדרש בידוד או לא
            isolation="בידוד ביעד: "
            if c["quarantineRules"]["duration"] != '':
                isolation+=str(c["quarantineRules"]["duration"])+ " ימי "+c["quarantineRules"]["text_he"]
            else:
                isolation+=c["quarantineRules"]["text_he"]
            information.append(isolation)
            # בדיקת קורונה ביעד
            corona_test="בדיקת קורונה ביעד: "
            corona_test+=c["covidTestRules"]["general_he"]
            information.append(corona_test)
            # עטיית מסכה
            mask="עטיית מסכה: "
            mask+=c["masks_he"]
            information.append(mask)
            # מסעדות
            rest="מסעדות: "
            rest+=c["restaurants_he"]
            information.append(rest)
            # אטרקציות
            attract="אטרקציות: "
            attract+=c["attractions_he"]
            information.append(attract)
            # תחבודה ציבורית
            trasp="תחבורה ציבורית: "
            trasp+=c["public_transportation_he"]
            information.append(trasp)
            update.message.reply_text('\n'.join(i for i in information), reply_markup=keyboard)
            return
    update.message.reply_text("המדינה לא נמצאה:("+"\n"+"נסה/י להקליד שנית" , reply_markup=keyboard)




