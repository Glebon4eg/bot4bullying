import asyncio
import json
import random
import time
import re
import os
import sys

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pathlib import Path


def restart_bot():
    os.execl(sys.executable, sys.executable, *sys.argv)


cfg_path = Path(__file__).parent / 'config.json'

# Считывание config.json
with open(cfg_path, "r") as cfg:
    try:
        config = json.load(cfg)
        if config["start_number"] == 1:
            config["API_ID"] = int(input("Введите API ID: "))
            config["API_HASH"] = str(input("Введите API HASH: "))
            config["start_number"] = 2
            with open(cfg_path, 'w') as cfg:
                json.dump(config, cfg, indent=2)
            restart_bot()
    except ValueError:
        print("Некорректно заполнен config.json! Пожалуйста, ознакомтесь с описанием и примером config файла на"
              " странице github и перепроверьте данные")
        exit()

slowmode = config["time_to_sleep"]
group_id = config["groupIDs"]
user_ids = config["userIDs"]
admin = config["Admin"]


def clear_config():
    config["groupIDs"] = []
    config["userIDs"] = []


# Авторизация в боте, два вторых аргумента нужны только при первом запуске
app = Client("my_account", api_id=config["API_ID"], api_hash=config["API_HASH"])


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
@app.on_message(filters.user(admin) & filters.reply & filters.command("add_userID"))
async def add_user(client, msg):
    if msg.reply_to_message.from_user.id not in user_ids:
        await msg.reply_text("User added!")
        config["userIDs"] += [msg.reply_to_message.from_user.id]
        print("New user was added: ", msg.reply_to_message.from_user.id)
        with open(cfg_path, 'w') as cfg:
            json.dump(config, cfg, indent=2)
    else:
        await msg.reply_text("User is already added!")


# Команда на исколючения человека из списка ПЛОХИШЕЙ
# Работает где угодно реплаем на нужного человека. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.reply & filters.command("remove_userID"))
async def remove_user(client, msg):
    if msg.reply_to_message.from_user.id in user_ids:
        await msg.reply_text("User removed!")
        config["userIDs"].remove(msg.reply_to_message.from_user.id)
        print("User was removed: ", msg.reply_to_message.from_user.id)
        with open(cfg_path, 'w') as cfg:
            json.dump(config, cfg, indent=2)
    else:
        await msg.reply_text("User not even in list!")


# Команда на добавление ID группы в список чатов, где бот будет работать
# Сработает в ТОЛЬКО чате и добавит его ID. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.group & filters.command("add_groupID"))
async def add_group(client, msg):
    if msg.chat.id not in group_id:
        await msg.reply_text("Group added!")
        config["groupIDs"] += [msg.chat.id]
        print("New group was added: ", msg.chat.id)
        with open(cfg_path, 'w') as cfg:
            json.dump(config, cfg, indent=2)
    else:
        await msg.reply_text("This group is already added!")


# Команда на исключения ID группы из списка чатов, где бот будет работать
# Сработает в ТОЛЬКО чате и уберет его ID. Доступна только админу(ам)
@app.on_message(filters.user(admin) & filters.group & filters.command("remove_groupID"))
async def remove_group(client, msg):
    if msg.chat.id in group_id:
        await msg.reply_text("Group removed!")
        config["groupIDs"].remove(msg.chat.id)
        print("Group was removed: ", msg.chat.id)
        with open(cfg_path, 'w') as cfg:
            json.dump(config, cfg, indent=2)
    else:
        await msg.reply_text("This group not even in list!")


# Добавление нового админа другими админами по его ID или тегу
@app.on_message(filters.command("add_admin") & filters.user(admin))
async def add_an_admin(client, msg):
    try:
        need = int(re.split(' ', msg.text)[1])
        # print(re.split(need))   # - Можно раскоментировать для проверки значения ID в консоли
        if need not in admin:
            await msg.reply_text("Admin added!")
            config["Admin"].append(need)
            print("New admin was added ", need)
            with open(cfg_path, 'w') as cfg:
                json.dump(config, cfg, indent=2)
        else:
            await msg.reply_text("Admin is already added!", quote=True)
    except ValueError:
        need = re.split(' ', msg.text)[1]
        if need not in admin:
            await msg.reply_text("Admin added!")
            config["Admin"] += [need]
            print("New admin was added", need)
            with open(cfg_path, 'w') as cfg:
                json.dump(config, cfg, indent=2)
        else:
            await msg.reply_text("Admin is already added!", quote=True)


# Перезагрузка бота командой(после внесения изменений в списках в конфиге самое то)
# Доступна только админу(ам)
@app.on_message(filters.command("restart") & filters.user(admin))
async def reboot(client, msg):
    await msg.reply_text("Be right back!", quote=True)
    restart_bot()


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
            await msg.reply_sticker(random.choice(config["stickers_pm"]), quote=True)
        elif config["answer_pm"] == "text":
            await msg.reply_text(config["text_pm"], quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)


# Нахождение ID человека. Работает в ТОЛЬКО личных сообщениях
@app.on_message(filters.private & ~filters.user(user_ids) & ~(filters.command("add_admin") & filters.user(admin)))
async def check(client, msg):
    if msg.forward_from is not None:
        await msg.reply_text(f"User ID: `{msg.forward_from.id}`", quote=True)
    elif (msg.forward_from is None) and (msg.from_user.first_name != msg.forward_sender_name is not None):
        await msg.reply_text("Forwarder's account is hidden, can't find an ID", quote=True)
    else:
        await msg.reply_text(f"Your User ID: `{msg.from_user.id}`", quote=True)


print("I am alive!")

if config["start_number"] == 2:
    first_admin = input("Введите свой @username или ID(его можно узнать у @useridinfobot) для добавления его в список "
                        "админов и дальнейшей настройки бота: ")
    try:
        config["Admin"] = [int(first_admin)]
    except ValueError:
        config["Admin"] = [str(first_admin)]
    config["start_number"] = 3
    clear_config()
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg, indent=2)
    restart_bot()

app.run()
