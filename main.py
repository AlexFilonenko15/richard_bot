import telebot
from dotenv import load_dotenv
import os
import schedule
import threading
import time

load_dotenv()
bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

TG_ID = []
counter = 2


def mess():
    global counter,TG_ID
    if TG_ID is not None:
        for id in TG_ID:
            if counter > 0:
                bot.send_message(id, f'До День Народження Папулькина Залишилося {counter} дня 🎂\nЯ Як Котик Не Можу вже Дочекатися 🥳', parse_mode='html')
                counter -= 1
            elif counter == 0:
                bot.send_message(id, 'День Народження Папульки настало 🎉🎉🎉\nВсі Вітаємо Нашого Імениника!!!', parse_mode='html')
                counter -= 1
            else:
                TG_ID.remove(id)
                bot.send_message(id, 'Жалко, що День Народження Так Швидко Закінчується 😢\nМи Всі Ще Раз Вітаємо Нашого Папулькина 🎉🎉🎉', parse_mode='html')
                


        


@bot.message_handler(commands=['send_message'])
def send_message(message):
    global counter
    if counter > 0:
        bot.send_message(message.chat.id, f'До День Народження Папулькина Залишилося {counter} дня 🎂\nЯ Як Котик Не Можу вже Дочекатися 🥳', parse_mode='html')
        counter -= 1
    else:
        bot.send_message(message.chat.id, 'День Народження Папульки настало 🎉🎉🎉\nВсі Вітаємо Нашого Імениника!!!', parse_mode='html')


@bot.message_handler(commands=['start_weakly_message'])
def weakly_message(message):
    global TG_ID
    if message.chat.id not in TG_ID:
        TG_ID.append(message.chat.id)
        bot.send_message(message.chat.id, 'Відлік До Папулькиного День Народження розпочато 🎁', parse_mode='html')
    elif message.chat.id in TG_ID:
        bot.send_message(message.chat.id, 'Відлік До Папулькиного День Народження вже розпочато 🎁', parse_mode='html')




@bot.message_handler(commands=['off_weakly_message'])
def off_message(message):
    if message.chat.id in TG_ID:
        TG_ID.remove(message.chat.id)
        bot.send_message(message.chat.id, 'Жалко, що День Народження Так Швидко Закінчується 😢\nМи Всі Ще Раз Вітаємо Нашого Папулькина 🎉🎉🎉', parse_mode='html')
    elif message.chat.id not in TG_ID:
        bot.send_message(message.chat.id, 'Відлік вже виключено.')



def scheduler():
    schedule.every(1).minutes.do(mess)

    while True:
        schedule.run_pending()
        time.sleep(1)



threading.Thread(target=scheduler, daemon=True).start()












bot.polling(none_stop=True)