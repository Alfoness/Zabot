from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import time

def get_cat_pic():
    api_url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(api_url)
    data = response.json()
    if data and isinstance(data, list) and 'url' in data[0]:
            image_url = data[0]['url']
            return image_url

async def generateKittyImage(client: Client, message: Message):
    await client.edit_message_text(chat_id=message.chat.id,
                                    text='**💬 Загрузка котика**',
                                    message_id=message.id)
    await client.send_photo(chat_id=message.chat.id, photo=get_cat_pic())
    await client.edit_message_text(chat_id=message.chat.id,
                                    text='**🥰 Милашка загрузилась!**',
                                    message_id=message.id)