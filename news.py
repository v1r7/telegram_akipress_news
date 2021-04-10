import telebot
import time
from key import key
from telebot import types
import requests
from bs4 import BeautifulSoup

user_dict = {}
bot = telebot.TeleBot(key)
akipress_url = 'https://kg.akipress.org'
list_of_news_categories = []
list_of_news_categories_dict = []
list_of_news=[]
list_of_news_categories_urls = []
mark_for_handler = [{'name': 'Продолжить'},
                    {'name': 'Выйти'}]

class LIST:
    def __init__(self, msg):
        self.msg = msg
        self.del_pr = None

@bot.message_handler(commands=["list"])
def any_msg(message):
    welcome_to_chanel = ('Akipress news у нас на Telegram канале')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row(mark_for_handler[0].get('name'),
               mark_for_handler[1].get('name'))
    msg = bot.send_message(message.chat.id, welcome_to_chanel,
                           reply_markup=markup)

    bot.register_next_step_handler(msg,
                                   callback_inline)

def callback_inline(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = LIST(message.text)
        if message.text == "Продолжить":
            list_welcome = 'Здесь вы можете выбрать подходящюю категорию ' \
                           'новостей'
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                       resize_keyboard=True)
            response = requests.get(akipress_url)
            soup = BeautifulSoup(response.text, 'lxml')
            soup = soup.find_all('div', class_='ptl_me_row_list')
            soup = soup[0].find_all('a')
            for s in soup:
                markup.add(s.text)
                f = s.text
                k = s.get("href")
                data = {
                    'name': f,
                    'url': f'{akipress_url}{k}'
                }
                list_of_news_categories_urls.append(f'{akipress_url}{k}')
                list_of_news_categories.append(s.text)
                list_of_news_categories_dict.append(data)
            msg = bot.send_message(chat_id,list_welcome,
                                   reply_markup=markup)
            bot.register_next_step_handler(msg,
                                           get_products_by_category
                                           )
        if message == "Выйти":
            time.sleep(20)
    except Exception as e:
        print(str(e))

def get_products_by_category(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = LIST(message.text)
        for category in list_of_news_categories_dict:
            if category.get('name') == message.text:
                markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                           resize_keyboard=True)
                response = requests.get(category.get('url'))

                soup = BeautifulSoup(response.text, 'lxml')
                soup = soup.find_all('div', class_='list')
                soup = soup[0].find_all('a')
                for i in soup:
                    markup.add(i.text)
                    k = i.get("href")
                    data = {
                        'name': i.text,
                        'url': f'{k}'}
                    list_of_news.append(data)
        msg = bot.send_message(chat_id,'Здесь вы можете найти '
                                       'самые актуальные новости на '
                                       'сегодняшний день',
                               reply_markup=markup)
        bot.register_next_step_handler(msg,get_finnaly_news)

    except Exception as e:
        print(str(e))

def get_finnaly_news(message):
    try:
        news_text = []
        chat_id = message.chat.id
        user_dict[chat_id] = LIST(message.text)
        for news in list_of_news:
            if news.get('name') == message.text:
                print(news.get('url'))
                response = requests.get(news.get('url'))
                soup = BeautifulSoup(response.text, 'lxml')
                soup = soup.find_all('div', class_="text")
                for s in soup:
                    news_text.append(s.text)
        bot.send_message(chat_id, news_text)
    except Exception as e:
        print(str(e))

bot.enable_save_next_step_handlers(delay=0)
bot.load_next_step_handlers()

bot.polling()