from pyrogram import Client, filters
from pyrogram.types import Message
from config import id
from pyrogram.enums import ChatType

meFilter = filters.create(
    name='yourselfContext',
    func=lambda args, flt, message: message.from_user.id == id
)

# Messages lib
addFavFilter = filters.create(
    name='specifyMessage',
    func=lambda args, flt, message: bool(message.from_user) and bool(message.text)  and message.from_user.id == id and message.text == "++"
)

addReactionFilter = filters.create(
    name="addUserToReactionModule",
    func=lambda args, flt, message: bool(message.from_user) and bool(message.text)  and message.from_user.id == id and message.text == "+r"
)

removeReactionFilter = filters.create(
    name="removeUserToReactionModule",
    func=lambda args, flt, message: bool(message.from_user) and bool(message.text) and message.from_user.id == id and message.text == "-r"
)

# KittyGenerator lib
ktyGeneratorFilter = filters.create(
    name='KittyGenerator',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.from_user.id == id and msg.text == "/cat"
)

# ChatManagement
cmBanFilter = filters.create(
    name='ban',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.from_user.id == id and msg.text == "/ban"
)

cmWarnFilter = filters.create(
    name='warn',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.from_user.id == id and msg.text == "/warn"
)

cmPromFilter = filters.create(
    name='promote',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.from_user.id == id and msg.text.startswith('/prom')
)

cmChatCreate = filters.create(
    name='chatCreate',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.from_user.id == id and msg.text.startswith('/cchat')
)

cmChatDelete = filters.create(
    name='chatDelete',
    func=lambda _, __, msg: bool(msg.from_user) and bool(msg.text) and msg.chat and msg.from_user.id == id and msg.text.startswith('/dchat')
)