from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from decouple import config
from pyrogram.types import Message
import Filters
import Source.messages as messages
import Source.kittyGenerator as ktyGen
import Source.chatManagement as cm

def main():
    # Init .env data 
    api_id = config('API_ID')
    api_hash = config('API_HASH')
    phone = config('PHONE')
    login = config('LOGIN')

    # Create pyrogram object and init params
    bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)

    # Include functions
    bot.add_handler(MessageHandler(messages.specifyMessage, Filters.addFavFilter))
    bot.add_handler(MessageHandler(messages.addUserToReactionModule, Filters.addReactionFilter))
    bot.add_handler(MessageHandler(messages.removeUserToReactionModule, Filters.removeReactionFilter))
    bot.add_handler(MessageHandler(ktyGen.generateKittyImage, filters=Filters.ktyGeneratorFilter))
    bot.add_handler(MessageHandler(cm.ban, Filters.cmBanFilter))
    bot.add_handler(MessageHandler(cm.warn, Filters.cmWarnFilter))
    bot.add_handler(MessageHandler(cm.promote, Filters.cmPromFilter))
    bot.add_handler(MessageHandler(cm.createChat, Filters.cmChatCreate))
    bot.add_handler(MessageHandler(cm.deleteChat, Filters.cmChatDelete))
    #bot.add_handler(MessageHandler())

    bot.add_handler(MessageHandler(messages.sendReaction, filters.text))    
    bot.run()

if __name__ == "__main__":
    main()