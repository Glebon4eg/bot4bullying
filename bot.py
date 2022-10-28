import asyncio
import json
import random
import time

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pathlib import Path

cfg_path = Path(__file__).parent / 'config.json'

# Считывание config.json
with open(cfg_path, "r") as cfg:
    try:
        config = json.load(cfg)
    except ValueError:
        print("Некорректно заполнен config.json! Пожалуйста, ознакомтесь с описанием config файла на странице github "
              "и перепроверьте данные")
        exit()

# TODO: добавить проверку на корректность конфига
"""
1) Создать список необходимых ключей
2) Получить список отсутствующих в конфиге ключей (полезна структура set)
3) Вызвать ошибку (assert / raise ValueError + вывести сообщение об ошибки вида: 
    "Ошибка: не хватает вот таких-то ключей")
"""

slowmode = config["time_to_sleep"]
group_id = config["groupIDs"]
user_ids = config["userIDs"]
admin = config["Admin"]

# Авторизация в боте, два вторых аргумента нужны только при первом запуске
app = Client("my_account", api_id=config["API_ID"], api_hash=config["API_HASH"])


# Отправка нужным людям в нужном чате один из стикеров из stickers_list на ВСЕ их сообщения
@app.on_message(filters.user(user_ids) & filters.chat(group_id))
async def doeb_cheloveka(client, msg):
    try:
        await msg.reply_sticker(random.choice(config["stickers_list"]))
        time.sleep(slowmode)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# Приветсвие новых пользователей
@app.on_message(filters.new_chat_members & filters.chat(group_id))
async def privet(client, new_m):
    try:
        await new_m.reply_sticker(random.choice(config["stickers_privet"]))
        time.sleep(slowmode)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# Ответ в личные сообщения нужным людям
@app.on_message(filters.user(user_ids) & filters.private)
async def pm(client, msg):
    try:
        if config["answer_pm"] == "sticker":
            await msg.reply_sticker(random.choice(config["stickers_pm"]))
        elif config["answer_pm"] == "text":
            await msg.reply_text(config["text_pm"])
    except FloodWait as e:
        await asyncio.sleep(e.value)


# Команда /ping
@app.on_message(filters.command("ping"))
async def pong(client, msg):
    try:
        await msg.reply_sticker(config["sticker_pong"])
        time.sleep(slowmode)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# Команда на добавление человека в список ПЛОХИШЕЙ. Работает в чате реплаем
# Работает где угодно реплаем на нужного человека. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.reply & filters.command("add"))
async def add(client, msg):
    config["userIDs"] += [msg.reply_to_message.from_user.id]
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg)


# Команда на исколючения человека из списка ПЛОХИШЕЙ
# Работает где угодно реплаем на нужного человека. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.reply & filters.command("remove"))
async def delete(client, msg):
    config["userIDs"].remove(msg.reply_to_message.from_user.id)
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg)


# Команда на добавление ID группы в список чатов, где бот будет работать
# Сработает в ТОЛЬКО чате и добавит его ID. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.group & filters.command("add_groupID"))
async def add_group(client, msg):
    config["groupIDs"] += [msg.chat.id]
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg)


# Команда на исключения ID группы из списка чатов, где бот будет работать
# Сработает в ТОЛЬКО чате и уберет его ID. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.group & filters.command("remove_groupID"))
async def remove_group(client, msg):
    config["groupIDs"].remove(msg.chat.id)
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg)


# Нахождение ID человека. Работает в ТОЛЬКО личных сообщениях
@app.on_message(filters.private & ~filters.user(user_ids))
async def check(client, msg):
    print(msg)
    if msg.forward_from is not None:
        need = "`" + str(msg.forward_from.id) + "`"
        await msg.reply_text("User ID: " + need, quote=True)
    elif (msg.forward_from is None) and (msg.from_user.first_name != msg.forward_sender_name) and (msg.forward_sender_name != None) :
        await msg.reply_text("Forwarder's account is hidden, can't find ID", quote=True)
    else:
        need = "`" + str(msg.from_user.id) + "`"
        await msg.reply_text("Your User ID: " + need, quote=True)


print("Я заработал")
app.run()
