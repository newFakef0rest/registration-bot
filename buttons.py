from telebot import types
from geopy import Nominatim


# Кнопки выбора
def choice():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton('Да')
    no = types.KeyboardButton('Нет')
    kb.add(yes, no)
    return kb


def phone():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(phone)
    return kb

def location():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)
    return kb
