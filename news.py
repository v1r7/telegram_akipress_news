import telebot
from key import key
from telebot import types
import requests
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(key)
akipress_url = 'https://kg.akipress.org/'
list_of_news_categories = []
list_of_news_categories_dict = []
urls = []


@bot.message_handler(commands=['start'])
def any_msg(message):
    welcome_to_chanel = ('Akipress news у нас на Telegram канале')
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text="Продолжить", callback_data="Продолжить")
    button2 = types.InlineKeyboardButton(text="Выйти", callback_data="Выйти")
    markup.add(button1, button2)
    print(markup)
    bot.send_message(chat_id=message.chat.id,
                     text=welcome_to_chanel,
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Продолжить":
            list_welcome = 'Здесь вы можете выбрать подходящюю категорию ' \
                           'новостей'
            response = requests.get(akipress_url)
            soup = BeautifulSoup(response.text, 'lxml')
            soup = soup.find_all('div', class_='ptl_me_row_list')
            soup = soup[0].find_all('a')
            for s in soup:
                f = s.text
                k = s.get("href")
                data = {
                    'name': f,
                    'url': f'https://kg.akipress.org{k}'
                }
                list_of_news_categories_dictionary = dict.fromkeys(s,f'https://kg.akipress.org{k}')
                list_of_news_categories.append(s.text)
                list_of_news_categories_dict.append(data)
                kbs = []
                for x in list_of_news_categories_dictionary.keys():
                    kbs = kbs + [InlineKeyboardButton(text=x, callback_data=list_of_news_categories_dictionary[x])]
                keyboard = InlineKeyboardMarkup(inline_keyboard=[kbs])
                print(keyboard)











        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Здесь вы можете выбрать подходящюю для вас '
                                   'категорию новостей',
                              reply_markup=keyboard
                              )







        if call.data == "Выйти":
            pass



bot.polling()