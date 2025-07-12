from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
import sqlite3
import config

database = sqlite3.connect('Data/chatMg.db', check_same_thread=False)
cursor = database.cursor()

async def ban(client: Client, message: Message):
    try:
        if message.reply_to_message:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await client.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.id,
                                        text=f"**📛 Пользователь - __{message.reply_to_message.from_user.first_name}__ забанен**")
        else:
            await client.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.id,
                                        text="**/ban** - исключить пользователя из группы")
    except Exception as E:
        print(E)

async def warn(client: Client, message: Message):
    try:
        if message.reply_to_message:
            id = message.from_user.id
            user = cursor.execute("SELECT * FROM warns WHERE id = ?", (id, )).fetchone()
            if user is None:
                cursor.execute("INSERT INTO warns (id, count) VALUES (?, ?)", (id, 1))
                database.commit()
                await client.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.id,
                                            text=f"⚠️ Пользователь - __{message.reply_to_message.from_user.first_name}__ получил своё первое предупреждение 1/3")
            else:
                warn = 0
                warn = int(user[1]) + 1
                if warn == 3:
                    cursor.execute("UPDATE warns SET count = ? WHERE id = ?", (0, id))
                    database.commit()
                    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                    await client.edit_message_text(chat_id=message.chat.id,
                                                message_id=message.id,
                                                text=f"**📛 Пользователь - __{message.reply_to_message.from_user.first_name}__ забанен, так как превысил кол-во предупреждений 3/3**")
                else:
                    cursor.execute("UPDATE warns SET count = ? WHERE id = ?", (warn, id))
                    database.commit()
                    await client.edit_message_text(chat_id=message.chat.id,
                                                message_id=message.id,
                                                text=f"⚠️ Пользователь - __{message.reply_to_message.from_user.first_name}__ получил предупреждение {warn}/3")
        else:
            await client.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.id,
                                        text="**/warn** - дать предупреждение пользователю")
    except Exception as E:
        print(E)

def checkFlags(flags: list, flag: str) -> bool:
    if flag in flags: return True
    else: return False

async def promote(client: Client, message: Message):
    if message.reply_to_message:
        try:
            flags = message.text.split(' ')
            privileges = ChatPrivileges(
                can_delete_messages=checkFlags(flags,'-dm'),     # Может удалять сообщения
                can_restrict_members=checkFlags(flags,'-rm'),    # Может банить пользователей
                can_pin_messages=checkFlags(flags,'-pin'),       # Может закреплять сообщения
                can_invite_users=checkFlags(flags,'-iu'),        # Может приглашать пользователей
                can_promote_members=checkFlags(flags,'-pm'),     # Не может назначать админов
                can_manage_chat=checkFlags(flags,'-mc'),         # Может управлять настройками чата
                can_manage_video_chats=checkFlags(flags,'-mvc'), # Может управлять видеозвонками
                can_change_info=checkFlags(flags,'-ci'),         # Может изменять информацию чата
                can_edit_messages=checkFlags(flags,'-em'),       # Может изменять сообщения
                is_anonymous=checkFlags(flags,'-an')             # Анонимный
            )
            await client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, privileges)
            if len(flags) > 1:
                await client.edit_message_text(chat_id=message.chat.id,
                                               message_id=message.id,
                                               text="✅ Пользователь получил статус администратора")
            else:
                await client.edit_message_text(chat_id=message.chat.id,
                                               message_id=message.id,
                                               text="✅ С пользователя снят статус администратора")
        except Exception as E:
            print(E)
    else:
        await client.edit_message_text(chat_id=message.chat.id,
                                       message_id=message.id,
                                       text="""
**/prom** - выдать участнику группы стутс администратора

  **-mc** - управление чатом
  **-dm** - удаление сообщений
  **-mvc** - управление гч
  **-rm** - управление участниками группы
  **-pm** - управление администраторами
  **-ci** - менять информацию чата
  **-pin** - прикреплять сообщения
  **-em** - изменять сообщения
  **-iu** - приглашать участников
  **-an** - анонимность администратора""")

async def createChat(client: Client, message: Message):
    try:
        chat = await client.create_group(title=message.text.split(' ')[1], users=config.id)
        link = await client.create_chat_invite_link(chat_id=chat.id)
        await client.edit_message_text(chat_id=message.chat.id,
                                       message_id=message.id,
                                       text=f"**ℹ️ Группа {chat.title} создана.\nВремя создания: {link.date}\nСсылка: **{link.invite_link}")
    except Exception as E:
        await client.edit_message_text(chat_id=message.chat.id,
                                       message_id=message.id,
                                       text=f'**/cchat <name> - создать группу с названием <name>. Будет добавлен только пользователь**\n🚫 Error {E}')

async def deleteChat(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        title = message.chat.title
        if len(message.text.split(" ")) == 2 and message.text.split(" ")[1] == title:
            await client.leave_chat(chat_id=chat_id, delete=True)
        elif len(message.text.split(" ")) == 2 and message.text.split(" ")[1] != title:
            await client.edit_message_text(chat_id=message.chat.id,
                                           message_id=message.id,
                                           text=f'**⚠️ Неправильно набрано название группы, введите /dchat {title} для удаления группы**')
        else:
            await client.edit_message_text(chat_id=message.chat.id,
                                           message_id=message.id,
                                           text='**/dchat <Название группы> - чтобы удалить группу, созданная вами.**')
    except Exception as E:
        print(E)