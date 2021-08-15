import requests
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup as bs
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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


def initialize_data_base():
    """
    insert the data to the data base from the API
    :return:
    """
    soup = import_pos_from_api()
    table = soup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')

    for row in rows:
        new_row = CovidTestingPositions(area=row.contents[1].get_text(strip=True),
                                        city=row.contents[3].get_text(strip=True))
        session = get_session()
        session.add(new_row)
        session.commit()


def get_session():
    return session_maker()

def testing_positions(update, context):
    """return list of testing positions according to the area"""
    pos = []
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


def get_testing_positions(update, context):
    buttons = [
        ['/NORTH'], ['/SOUTH'], ['/CENTER'], ['/JERUSALEM'], ['/menu']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('באיזה אזור תרצה לבצע בדיקה?')
    update.message.reply_text('צפון (/NORTH)'+'\n'+'דרום (/SOUTH)'+'\n'+'מרכז (/CENTER)'+'\n'+'ירושלים (/JERUSALEM)'+'\n', reply_markup=keyboard)

def import_pos_from_api():
    page = requests.get(
        "https://www.leumit.co.il/heb/Life/FamilyHealth/familyhealth/coronavirus/CoronaTesting1/articlegalleryitem,3967/")
    return bs(page.content, features="html.parser")










