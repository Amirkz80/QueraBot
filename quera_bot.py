from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from jobs_asycn import run_program
from dotenv import load_dotenv
import os


load_dotenv()

# The bot token
tkn = str(os.getenv('TOKEN'))

# Defining bot updator and dispatcher

updater = Updater(tkn, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start_command(update : Update, context : CallbackContext) :
    """Answers and encourage user to start using the bot through a message"""
    start_text = "سلام، تکنولوژی مورد نظرت رو برای من بفرست تا داخل کوئرا به دنبالش بگردم ، با استفاده از دستور /list میتونی ببینی از چه تکنولوژی هایی پشتیبانی میکنم 😃"
    start_text += ".\n\nبا استفاده از دستور /help میتونی با طرز کار ربات آشنا بشی"
    start_text += "🤖"
    context.bot.send_message(chat_id = update.effective_chat.id, text = start_text )

def list_command(update : Update, context : CallbackContext) :
    """Shows valid technologies list"""
    intro_message = "زبان ها و تکنولوژی هایی که می تونی بر اساس اونا در کوئرا به دنبال آگهی های شغلی مورد نظرت بگردی 🔍😀 :"
    context.bot.send_message(chat_id = update.effective_chat.id, text = intro_message)
    valid_technologies = "backend🤓\nfrontend👨🏻‍🎨\nmobile📱\njavascript🤯\nreact⚛️\npython🐍\nphp🐘\nlaravel🏰\nC#🏋🏻‍♂️\ndjango🎺\njava☕️\ndocker🐳\ntypescript⌨️\nvue.js🥷🏻\nlinux🐧\nredux☢️\nangular🛡\npostgresql🐘\nrest✉️\nnode.js👨🏻‍💻"
    context.bot.send_message(chat_id = update.effective_chat.id, text = valid_technologies)

def help_command(update : Update, context : CallbackContext) :
    """Describes how does the bot work"""
    help_text = 'برای استفاده از بات کافیه تا دستور /list رو وارد کنی . بعد از اون کافیه تا تکنولوژی یا تکنولوژی های مورد نظرتو از داخل لیست انتخاب کنی و برای من بفرستی. برای مثال اگه گزینه پایتون رو انتخاب میکنی صرفا بنویس python و برای من پیام بفرست '
    help_text += '\n\n اگر تکنولوژی هایی که مد نظرت هستن از یکی بیشتر بودن کافیه تا اونارو با یه فاصله بینشون برای من بفرستی. برای مثال اگه java و python و javascript و php رو انتخاب کردی ، کافیه تا بنویسی : java python javascript php'
    help_text += '\n\nامیدوارم جست و جوی موفقی داشته باشی 😉👍🏻'
    context.bot.send_message(chat_id = update.effective_chat.id, text = help_text)

def send_article(update : Update, context : CallbackContext) :
    """Gets text from user and returns it ti h/h"""
    jobs =  run_program(update.message.text.lower())
    jobs_list = list(jobs)
    jobs_message = ''

    # telegram has limitation in sending messages(4096 characters) so let's see if our message has more than 15 articels
    if len(jobs) > 15:
        two_pages_amount = int(len(jobs)/15)

        # brake our message into several messages which each one has 15 articels in it
        cycle = 0
        for i in range(1, two_pages_amount + 1):
            jobs_message = f"صفحه {i}\n\n"
            for j in range(cycle, cycle + 15):
                jobs_message += "\n"
                jobs_message += f"عنوان آگهی👨🏻‍💻👩🏻‍💻 = {jobs[jobs_list[j]][1]}\nلینک🏃🏻‍♂️🏃🏻‍♀️ = {jobs[jobs_list[j]][0]}\n\n"
                
            cycle += 15
            context.bot.send_message(update.effective_chat.id, jobs_message)
            jobs_message = ''

        # See if we have any remaining (not full page) or not
        if len(jobs) > cycle:

            jobs_message = f"صفحه {two_pages_amount + 1}\n\n"
            for i in range(cycle, len(jobs)):
                jobs_message += "\n"
                jobs_message += f"عنوان آگهی👨🏻‍💻👩🏻‍💻 = {jobs[jobs_list[i]][1]}\nلینک🏃🏻‍♂️🏃🏻‍♀️ = {jobs[jobs_list[i]][0]}\n\n"


            context.bot.send_message(update.effective_chat.id, jobs_message)

    else:

        if jobs_list:
            i = 1
            jobs_message += f"صفحه {i}\n\n" 
            for value in jobs.values():
                jobs_message += "\n"
                jobs_message += f"عنوان آگهی👨🏻‍💻👩🏻‍💻 = {value[1]}\nلینک🏃🏻‍♂️🏃🏻‍♀️ = {value[0]}\n\n"

            context.bot.send_message(update.effective_chat.id, jobs_message)


def unkown_command(update : Update, context : CallbackContext) :
    """replies to unkown commands"""
    context.bot.send_message(chat_id = update.effective_chat.id, text = "متاسفم این دستور معتبر نیست :( لطفا از لیست دستورات گزینه دلخواه را انتخاب کنید.")

command_handler = CommandHandler(['start'], callback = start_command, filters = ~Filters.update.edited_message)
list_command_handler = CommandHandler(['list'], callback = list_command, filters = ~Filters.update.edited_message)
help_command_handler = CommandHandler(['help'], callback = help_command, filters = ~Filters.update.edited_message)
message_handler = MessageHandler(filters = Filters.text & (~Filters.command) ,callback = send_article)
unkown_handler = MessageHandler(filters = Filters.command, callback = unkown_command)

dispatcher.add_handler(command_handler)
dispatcher.add_handler(list_command_handler)
dispatcher.add_handler(help_command_handler)
dispatcher.add_handler(unkown_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()