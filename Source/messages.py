from pyrogram import Client, filters
from pyrogram.types import Message

from datetime import datetime
import pytz
import sqlite3
import random

fvData = sqlite3.connect(database='Data/fvData.db', check_same_thread=False)
crFvData = fvData.cursor()

UserFilter = sqlite3.connect(database='Data/UsersFilter.db', check_same_thread=False)
crUserFilter = UserFilter.cursor()

async def specifyMessage(client: Client, message: Message):
    id = message.reply_to_message.id
    user_id = message.reply_to_message.from_user.id
    user_fname = message.reply_to_message.from_user.first_name
    user_lname = message.reply_to_message.from_user.last_name
    user_username = message.reply_to_message.from_user.username
    message_text = message.reply_to_message.text
    publish_date = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M:%S')
    crFvData.execute("INSERT INTO messages (id, user_id, user_fname, user_lname, user_username, message_text, publish_date) VALUES (?,?,?,?,?,?,?)", (id, user_id, user_fname, user_lname, user_username, message_text, publish_date))
    fvData.commit()
    await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='**✅ Сообшение сохраненно**')

async def sendReaction(client: Client, message: Message):
    try:
        if crUserFilter.execute("SELECT id FROM reactions WHERE id = ?", (message.from_user.id, )).fetchone() is not None:
            #reaction = random.choice(crUserFilter.execute("SELECT emojies FROM settings").fetchone()[0][2])
            await client.send_reaction(chat_id=message.chat.id, message_id=message.id, emoji='👍')
    except AttributeError:
        pass

async def addUserToReactionModule(client: Client, message: Message):
    try:
        id = message.reply_to_message.from_user.id
        crUserFilter.execute("INSERT INTO reactions (id) VALUES (?)", (id, ))
        UserFilter.commit()
        await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='**✅ Пользователь добавлен в список**')
    except:
        await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='**⁉️ Пользователь не найден**')

async def removeUserToReactionModule(client: Client, message: Message):
    try:
        id = message.reply_to_message.from_user.id
        crUserFilter.execute("DELETE FROM reactions WHERE id = ?", (id, ))
        UserFilter.commit()
        await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='**✅ Пользоватенль убран из списка**')
    except:
        await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='**⁉️ Пользователь не найден**') 