#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
#import pypyodbc as pyodbc
import datetime

import telebot
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InlineQuery,
                           InlineQueryResultArticle, InputTextMessageContent)
from telebot import types
from time import time, sleep

import settings
import random
import re

import sqlite3

# Insert your telegram bot`s token here
TOKEN = settings.Telegram.TOKEN
bot = telebot.TeleBot(TOKEN)

# bot's consts
#ELEMENTS_ON_PAGE = 7
ELEMENTS_ON_PAGE = 1
BOOKS_CHANGER = 5






@bot.callback_query_handler(func=lambda x: re.search(r'b_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(r'C:\Users\ivan\avito.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Ссылканаавито FROM chatbot")
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books is None:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        #return
    if books is not None:
        bot.edit_message_text('данных есть', chat_id=msg.chat.id, message_id=msg.message_id)
        #return
    bot.send_chat_action(msg.chat.id, 'typing')
    try:
        _, page = callback.data.split('_')
        #page = callback.data.split('_')
    except ValueError as err:
        print('ошибка')
        return
    page = int(page)
    if len(books) % ELEMENTS_ON_PAGE == 0:
        page_max = len(books) // ELEMENTS_ON_PAGE
    else:
        page_max = len(books) // ELEMENTS_ON_PAGE + 1
    msg_text = ''
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
    msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'b')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode='HTML')


def get_keyboard(page: int, pages: int, t: str) -> InlineKeyboardMarkup or None:  # make keyboard for current page
    if pages == 1:
        return None
    keyboard = InlineKeyboardMarkup()
    row = []
    if page == 1:
        row.append(InlineKeyboardButton('≻', callback_data=f'{t}_2'))
        if pages >= BOOKS_CHANGER:
            next_l = min(pages, page + BOOKS_CHANGER)
            row.append(InlineKeyboardButton(f'{next_l} >>',
                                            callback_data=f'{t}_{next_l}'))
        keyboard.row(*row)
    elif page == pages:
        if pages >= BOOKS_CHANGER:
            previous_l = max(1, page - BOOKS_CHANGER)
            row.append(InlineKeyboardButton(f'<< {previous_l}',
                                            callback_data=f'{t}_{previous_l}'))
        row.append(InlineKeyboardButton('<', callback_data=f'{t}_{pages-1}'))
        keyboard.row(*row)
    else:
        if pages >= BOOKS_CHANGER:
            next_l = min(pages, page + BOOKS_CHANGER)
            previous_l = max(1, page - BOOKS_CHANGER)

            if previous_l != page - 1:
                row.append(InlineKeyboardButton(f'<< {previous_l}',
                                                callback_data=f'{t}_{previous_l}'))

            row.append(InlineKeyboardButton('<', callback_data=f'{t}_{page-1}'))
            row.append(InlineKeyboardButton('>', callback_data=f'{t}_{page+1}'))

            if next_l != page + 1:
                row.append(InlineKeyboardButton(f'{next_l} >>',
                                                callback_data=f'{t}_{next_l}'))
            keyboard.row(*row)
        else:
            keyboard.row(InlineKeyboardButton('<', callback_data=f'{t}_{page-1}'),
                         InlineKeyboardButton('>', callback_data=f'{t}_{page+1}'))
    return keyboard

@bot.message_handler(func=lambda message: True)
def search(msg: Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('По названию', callback_data='b_1'),
                 )
    bot.reply_to(msg, 'Поиск: ', reply_markup=keyboard)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(str(e))
            #print(e.message)
            sleep(5)
            continue
            #non stop polling not looking at error
    


