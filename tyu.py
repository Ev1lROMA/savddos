import telebot
from telebot import types
import random
import requests, json
from bs4 import BeautifulSoup
import requests
import csv
import numpy as np
import pandas as pd
import os
import io
import os.path
import time
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
import webbrowser as w
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

bot = telebot.TeleBot('6001371855:AAGDdoRBQs_W18ccVuBof3l_ENHOgGXT28o')

inline_but1 = types.InlineKeyboardButton('Поиск товара', callback_data='Main_btn')
inline_but2 = types.InlineKeyboardButton('Wishlist', callback_data='w_btn')
inline_b1 = types.InlineKeyboardMarkup().add(inline_but2).add(inline_but1)

inline_type2_b1 = types.InlineKeyboardButton('Перейти по ссылке', callback_data='link_btn')
inline_type2_b2 = types.InlineKeyboardButton('Посмотреть следующий товар', callback_data='next_btn')
inline_type2_b3 = types.InlineKeyboardButton('Вернуться назад', callback_data='back_btn')
inline_type2_b4 = types.InlineKeyboardButton('Добавить в виш лист', callback_data='Wish_btn')
inline_b2 = types.InlineKeyboardMarkup().add(inline_type2_b1).add(inline_type2_b2).add(inline_type2_b3).add(inline_type2_b4)

pr = []
i = 0
url_item = ""


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, f'Приветствую, <b>{message.from_user.first_name}</b>, я твой бот по подбору техники. Выбери пункт, который тебя заинтересовал.', parse_mode='html', reply_markup=inline_b1)


@bot.callback_query_handler(func=lambda c: c.data == 'Main_btn')
def process_callback_1(callback_query: types.CallbackQuery):
    global i
    i = 0
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Введи название товара, который ты хочешь посмотреть')


@bot.callback_query_handler(func=lambda c: c.data == 'link_btn')
def link_button(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda c: c.data == 'next_btn')
def next_button(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    next_link(callback_query)


def next_link(callback_query):
    global i
    i += 1
    inline_type2_b1.url = '{}'.format(pr[i][0])
    bot.send_message(callback_query.from_user.id, '{} товара и цена'.format(pr[i][1]), reply_markup=inline_b2)


@bot.callback_query_handler(func=lambda c: c.data == 'back_btn')
def proc_back(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Вы вернулись на главную страницу. Выберите пункт', reply_markup=inline_b1)


@bot.callback_query_handler(func=lambda c: c.data == 'Wish_btn')
def proc_wish(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    addWish(pr[i][0], callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Товар добавлен в виш лист', reply_markup=inline_b1)


@bot.callback_query_handler(func=lambda c: c.data == 'w_btn')
def w_button(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    show_wishlist(callback_query)


def show_wishlist(idChat):
    with io.open('WishList.csv', encoding="utf-8") as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for l in file_reader:
            if l[3] == idChat:
                s = 'Наименование товара -' + l[2] + '\nСтоимость товара на данный момент -' + l[1] + "\nСсылка на товар -" + l[0]
                bot.send_message(idChat, s, reply_markup=inline_b1)


def contains(temp):
    if os.stat('WishList.csv').st_size != 0:
        with io.open('WishList.csv', encoding="utf-8") as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for l in file_reader:
                if l == temp:
                    return True
    return False


def addWish(url_magazine, idChat):
    linq_price = []
    response = requests.get(url_item)
    linq_name = ""
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('div', {'class':'page-title'}):
        linq_name = link.get('data-title')
    for link1 in soup.findAll(class_='where-buy-price'):
        linq_price.append(link1.text.split()[0]+"р")
    temp = [url_magazine, linq_price[1], linq_name, idChat]
    if contains(temp) == False:
        with io.open('WishList.csv', mode='a', newline='', encoding="utf-8") as r_file:
            file_writer = csv.writer(r_file, delimiter=",")
            file_writer.writerow(temp)


def update():
    time_s = time.time()
    while(True):
        time_stop = time.time()
        if(time_s - time_stop == 86400):
           time_s = time.time()
           with io.open('WishList.csv', mode='a', newline='', encoding="utf-8") as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                for l in file_reader:
                    linq_price = []
                    response = requests.get(l[0])
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for link in soup.findAll(class_='where-buy-price'):
                        linq_price.append(link.text.split()[0]+"р")
                    #if linq_price[0] < l[1]:
                        #file_reader[] = linq_price[0]


def parse_name(m):
    response = requests.get(m)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find('h1', class_='title-for-page').text
    return data


def parse_price(m):
    response = requests.get(m)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find('h1', class_='title-for-page').text
    return data


def parse(str):
    linq_list = []
    linq_name = ""
    temp = []
    response = requests.get("https://n-katalog.ru/search?keyword=" + str)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a', {'class': 'model-all-shops ib'}):
        temp = parse_linq("https://n-katalog.ru" + link.get('href'))
        response2 = requests.get("https://n-katalog.ru" + link.get('href'))
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        for link1 in soup2.findAll('div', {'class': 'page-title'}):
            linq_name = link1.get('data-title')
        for l in temp:
            linq_list.append([l, linq_name])
        #linq_list.append(parse_linq("https://n-katalog.ru" + link.get('href')))
    return linq_list


def parse_linq(href):
    linq_list = []
    global url_item
    url_item = href
    response = requests.get(href)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a', {'class': 'yel-but-2'}):
        linq_list.append("https://n-katalog.ru" + link.get('onmouseover').split(sep='"')[1])
    return linq_list


@bot.message_handler(content_types=['text'])
def reply(message):
    global pr
    pr = parse(message.text.replace(' ', '+'))
    inline_type2_b1.url = '{}'.format(pr[i][0])

    bot.send_message(message.from_user.id, '{} и цена товара'.format(pr[i][1]), reply_markup=inline_b2)


bot.polling(none_stop=True)

