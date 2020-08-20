import telebot
import config
import dbworker
import time
import sqlite3
import datetime
from vedis import Vedis
import re

bot = telebot.TeleBot(config.token)
keyboard_1 = telebot.types.ReplyKeyboardMarkup()
keyboard_1.row('Add user', 'Next pay')
pattern = r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello, you sey me /hello", reply_markup=keyboard_1)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def add_user(message):
    if message.text.lower() == 'add user':
        bot.send_message(message.chat.id, 'Введіть дату вашої наступної проплати. (dd.mm.yyyy)')
        dbworker.set_state(message.chat.id, config.States.S_ENTER_DATE.value)
    else:
        bot.send_message(message.chat.id, 'Помилка!!! Оберіть додати користувача')


@bot.message_handler(func=lambda message: dbworker.get_current_state(
    message.chat.id) == config.States.S_ENTER_DATE.value)
def user_entering_name(message):
    date = message.text
    try:
        valid_date = re.search(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d', message.text)
        chat_id = message.chat.id
        conn = sqlite3.connect("reminder.db")
        cursor = conn.cursor()
        sql = '''INSERT INTO user_family(user_id, next_payment) VALUES(?, ?)'''
        cursor.execute(sql, (chat_id, date))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Чудово! Користувача додано.")
        dbworker.set_state(message.chat.id, config.States.S_GET_DATE.value)
    except ValueError:
        bot.send_message(message.chat.id, "Проблема з форматом вводу дати. Спробуй ще раз.")
        bot.send_message(message.chat.id, '(dd/mm/yyyy)')


@bot.message_handler(func=lambda message: dbworker.get_current_state(
    message.chat.id) == config.States.S_GET_DATE.value)
def get_date(message):
    if message.text.lower() == 'next pay':
        chat_id = message.chat.id
        conn = sqlite3.connect("reminder.db")
        cursor = conn.cursor()
        cursor.execute("SELECT next_payment FROM user_family WHERE user_id=?", (chat_id,))
        date = cursor.fetchall()
        conn.close()
        bot.send_message(message.chat.id, date)




def remind():
    now = datetime.datetime.now()
    conn = sqlite3.connect("reminder.db")
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT * FROM user_family')
    rows = cursorObj.fetchall()
    for row in rows:
        time = row[2]
        target_date = datetime.datetime.strptime(time, "%d.%m.%Y")
        diff = target_date - now
        print(diff)
        if diff.days <= 2:
            chat_id = row[1]
            bot.send_message(chat_id, 'Нагадування!!! Проплата AppleMusic через 2 дня.')


bot.polling()
