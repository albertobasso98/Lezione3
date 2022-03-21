#pip install python-telegram-bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import secret
from secret import bot_token, password

logged_user = []

def welcome(update, context):
    user = update.message.from_user
    if user['id'] not in logged_user:
        msg = '''Welcome in <b>My Bot</b>Send password to authenticate'''
        update.message.reply_text(msg, parse_mode='HTML')
    else:
        msg = '''Welcome in <b>My Bot</b>'''
        update.message.reply_text(msg, parse_mode='HTML')

def process_chat(update, context):
    user = update.message.from_user
    if update.message.text.lower() == secret.password:
        logged_user.append(user['id'])
        update.message.reply_text('Welcome you have been logged', parse_mode='HTML')
    if user['id'] not in logged_user:
        welcome(update, context)
    elif update.message.text.lower() == 'avvisi':
        msg = 'Non ci sono nuovi avvisi'
        update.message.reply_text(msg, parse_mode='HTML')
    elif update.message.text.lower() == 'graph':
        chat_id = update.message.chat.id
        context.bot.send_document(chat_id=chat_id, document=open('photo.jpg', 'rb'))
    else:
        welcome(update, context)

def process_location(update, context):
    user = update.message.from_user
    if user['id'] not in logged_user:
        welcome(update, context)
    else:
        if update.edited_message:
            message = update.edited_message
        else:
            message = update.message

        user_location = message.location

        user = message.from_user
        print(user)
        print(f"You talk with user {user['first_name']} and his user ID: {user['id']}")

        msg = f'Ti trovi presso lat={user_location.latitude}&lon={user_location.longitude}'
        print(msg)
        message.reply_text(msg)

def photo_handler(update, context):
    user = update.message.from_user
    if user['id'] not in logged_user:
        welcome(update, context)
    else:
        file = context.bot.getFile(update.message.photo[-1].file_id)
        file.download('photo.jpg')
        update.message.reply_text('photo received')

def main():
   print('bot started')
   upd= Updater(bot_token, use_context=True)
   disp=upd.dispatcher

   disp.add_handler(CommandHandler("start", welcome))
   disp.add_handler(MessageHandler(Filters.regex('^.*$'), process_chat))
   disp.add_handler(MessageHandler(Filters.location, process_location))
   disp.add_handler(MessageHandler(Filters.photo, photo_handler))


   upd.start_polling()
   upd.idle()



if __name__=='__main__':
   main()