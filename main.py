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

#sqllite
dbpath=r'C:\Users\user\avito.db'


menuback = u'\U0001F519'

#'Юг'           - a ap ag az
#'Север'        - b bp bg bz
#'Восток'       - c cp cg cz
#'Запад'        - d cd cg cz
#'Брянск'       - e ed eg ez
#'Кострома'     - f fd fg fz
#'Иваново'      - g gd gg gz
#'Тверь'        - h hd hg hz
#'Тула'         - i id ig iz   
#'Смоленск'     - j jd jg jz
#'Рязань'       - k kd kg kz
#'Калуга'       - m md mg mz

#Помещение - p
#Гараж - g
#Здание - z


@bot.callback_query_handler(func=lambda x: re.search(r'ap_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE (Регион = ? or Регион = ? or Регион = ? or Регион = ? )and Типобъекта = ?''', ("Юг","Север","Запад","Восток","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ap')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'ag_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    #cursor.execute('''SELECT Ссылканаавито FROM chatbot
    #                      WHERE Регион = ? and Типобъекта = ?''', ("Юг","Гараж",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE (Регион = ? or Регион = ? or Регион = ? or Регион = ? )and Типобъекта = ?''', ("Юг","Север","Запад","Восток","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ag')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'az_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    #cursor.execute('''SELECT Ссылканаавито FROM chatbot
    #                      WHERE Регион = ? and Типобъекта = ?''', ("Юг","Здание",))
    
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE (Регион = ? or Регион = ? or Регион = ? or Регион = ? )and Типобъекта = ?''', ("Юг","Север","Запад","Восток","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'az')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')


@bot.callback_query_handler(func=lambda x: re.search(r'ep_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Брянск","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ep')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'eg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Брянск","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'eg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'ez_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Брянск","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ez')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')



@bot.callback_query_handler(func=lambda x: re.search(r'fp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Кострома","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'fp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'fg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Кострома","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'fg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'fz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Кострома","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'fz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')



@bot.callback_query_handler(func=lambda x: re.search(r'gp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Иваново","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'gp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'gg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Иваново","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'gg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'gz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Иваново","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'gz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')


@bot.callback_query_handler(func=lambda x: re.search(r'hp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тверь","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'hp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'hg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тверь","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'hg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'hz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тверь","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'hz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')



@bot.callback_query_handler(func=lambda x: re.search(r'ip_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тула","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ip')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'ig_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тула","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'ig')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'iz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Тула","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'iz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')


@bot.callback_query_handler(func=lambda x: re.search(r'jp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Смоленск","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'jp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'jg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Смоленск","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'jg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'jz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Смоленск","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'jz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')


@bot.callback_query_handler(func=lambda x: re.search(r'kp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Рязань","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'kp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'kg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Рязань","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'kg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'kz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Рязань","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'kz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')


@bot.callback_query_handler(func=lambda x: re.search(r'mp_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Калуга","Помещение",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'mp')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'mg_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Калуга","Гараж",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books == []:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'mg')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda x: re.search(r'mz_([0-9])+', x.data) is not None)
def search_by_title(callback: CallbackQuery):  # search books by title
    msg = callback.message
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    #cursor.execute("SELECT Ссылканаавито,Номер FROM chatbot")
    #cursor.execute('''SELECT Ссылканаавито,Номер FROM chatbot
    #                  WHERE Регион = ?''',("Юг",))
    cursor.execute('''SELECT Ссылканаавито FROM chatbot
                          WHERE Регион = ? and Типобъекта = ?''', ("Калуга","Здание",))
    # Получаем результат сделанного запроса
    books = cursor.fetchall()
    conn.close()
    if books ==[]:
        bot.edit_message_text('нет данных', chat_id=msg.chat.id, message_id=msg.message_id)
        return
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
    msg_text += f'<code>Страница {page}/{page_max}</code>'
    for book in books[ELEMENTS_ON_PAGE * (page - 1):ELEMENTS_ON_PAGE * page]:
        #msg_text += book[0]
        msg_text += '<a href="'+book[0]+'">'+book[0]+'</a>\n'
        
    #msg_text += f'<code>Страница {page}/{page_max}</code>'    
    keyboard = get_keyboard(page, page_max, 'mz')
    if keyboard:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(msg_text, chat_id=msg.chat.id,disable_web_page_preview=False, message_id=msg.message_id, parse_mode='HTML')



#'Юг'           - a ap ag az
#'Север'        - b bp bg bz
#'Восток'       - c cp cg cz
#'Запад'        - d cd cg cz

#'Московская об' - a ap ag az
#'Брянск'       - e ed eg ez
#'Кострома'     - f fd fg fz
#'Иваново'      - g gd gg gz
#'Тверь'        - h hd hg hz
#'Тула'         - i id ig iz   
#'Смоленск'     - j jd jg jz
#'Рязань'       - k kd kg kz
#'Калуга'       - m md mg mz

#Помещение - p
#Гараж - g
#Здание - z







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



#Меню

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message:message.text == 'Меню')
@bot.message_handler(func=lambda message:message.text == 'меню')
@bot.message_handler(func=lambda message:message.text == 'Меню'+menuback)
def search(msg: Message):
    #photo = open(r'C:\Users\ivan\Desktop\avitobot\photo\1.jpg', 'rb')
    #bot.send_photo(msg.chat.id,photo,caption="Недвига")
    #bot.send_message(msg.chat.id,'<a href="http://www.planwallpaper.com/static/images/i-should-buy-a-boat.jpg"></a>',parse_mode='HTML')
    #Здесь создаем меню
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Московская область')
    markup.add('Брянская об.','Костромская об.')
    markup.add('Ивановская об. ','Тверская об.')
    markup.add('Тульская об.','Смоленская об.')
    markup.add('Рязанская об.','Калужская об.')
    markup.add('Меню'+menuback)
    msg = bot.send_message(msg.chat.id, 'Выберите территорию для просмотра недвижимости:', reply_markup=markup)
  

@bot.message_handler(func=lambda message:message.text == 'Московская область')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='ap_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='ag_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='az_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

@bot.message_handler(func=lambda message:message.text == 'Брянская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='ep_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='eg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='ez_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

    

@bot.message_handler(func=lambda message:message.text == 'Костромская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='fp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='fg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='fz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 



@bot.message_handler(func=lambda message:message.text == 'Ивановская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='gp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='gg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='gz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

@bot.message_handler(func=lambda message:message.text == 'Тверская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='hp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='hg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='hz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

@bot.message_handler(func=lambda message:message.text == 'Тульская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='ip_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='ig_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='iz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

@bot.message_handler(func=lambda message:message.text == 'Смоленская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='jp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='jg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='jz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 
    

@bot.message_handler(func=lambda message:message.text == 'Рязанская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='kp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='kg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='kz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Или выйдите в меню:', reply_markup=markup) 

@bot.message_handler(func=lambda message:message.text == 'Калужская об.')
def handter(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Помещение', callback_data='mp_1'))
    keyboard.add(InlineKeyboardButton('Гараж', callback_data='mg_1'))
    keyboard.add(InlineKeyboardButton('Задание', callback_data='mz_1'))
    bot.reply_to(message, 'Выберите тип объекта: ', reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'для выхода в меню:', reply_markup=markup) 


#инструкция

@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message:'Помощь' == message.text, content_types=['text'])
def processinstr(message):
    #отправлем инструкцию
    bot.send_message(message.chat.id,"""Вас приветствует чат-бот СРБ!.
    Я покажу вам коммерческую недвижимость СРБ!
                       Инструкция
    Для начала общения со мной, пришлите мне /start,
    или нажмите на кнопку """+menuback+"""Меню
    Свои пожелания можете писать разрботчику:@Hugmymind в телеграмме
    """)
    #отправлем обратно меню
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
    markup.add('Меню'+menuback)
    bot.send_message(message.chat.id, 'Нажмите Меню,чтобы выйти в меню', reply_markup=markup)


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
    

