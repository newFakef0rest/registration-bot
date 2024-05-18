import telebot, buttons, database
from geopy import Nominatim

bot = telebot.TeleBot('7084406107:AAH6l8dEaqpDBt62_qI1-Dbhkfef73shhn8')

geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/124.0.0.0 Safari/537.36')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = database.check_user(user_id)
    if check:
        bot.send_message(user_id, f'Добро пожаловать {message.from_user.first_name}')
    else:
        bot.send_message(user_id, f'Привет {message.from_user.first_name}')
        bot.send_message(user_id, f'Желаете пройти регистрацию?', reply_markup=buttons.choice())
        bot.register_next_step_handler(message, text)

@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.from_user.id
    if message.text.lower() == 'да':
        bot.send_message(user_id, 'Введите ваше имя и фамилию')
        bot.register_next_step_handler(message, yes)
    else:
        bot.send_message(user_id, 'пидора ответ')
        bot.register_next_step_handler(message, start)

def yes(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f'Ваше имя и фамилия: {name}')
    get_phone(message, name)


def get_phone(message, name):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Теперь нужен ваш номер телефона', reply_markup=buttons.phone())
    bot.register_next_step_handler(message, get_num, name)

def get_num(message, name):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Теперь скиньте локацию', reply_markup=buttons.location())
        bot.register_next_step_handler(message, get_location, name, user_num)
    else:
        bot.send_message(user_id, 'Отправьте ваш номер')
        bot.register_next_step_handler(message, get_num, name)

def get_location(message, name, user_num):
    user_id = message.from_user.id
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.latitude}, {message.location.longitude}')
        database.register(user_id, name, user_num, str(user_loc))
        bot.send_message(user_id, 'Отлично, вы прошли регистрацию!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте локацию')
        bot.register_next_step_handler(message, get_location, name, user_num)



bot.polling()
