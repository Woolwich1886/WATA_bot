import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import random
import Fixture
import Tabloid

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
token = 'мой токен'
command_list = '/welcome - приветствие \n/help - список команд \n/next - следующий матч\n/table - таблица АПЛ'


# Приветствие
def Welcome(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет, {})".format(update.message.from_user.first_name))
# Список команд
def Help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=command_list)

# Таблица апл картинкой
def Table(bot, update):
    bot.send_photo(chat_id=update.message.chat_id,
                     photo=open('test.png', 'rb'))

# Следующий матч
def Next(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=Fixture.find_next_game())


def tth(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='https://youtu.be/GdBYkDB5AEU')


# Повторяет за юзером
def What_you_say(bot, update):
    def random_answer():
        answer_set = {
            'Не думаю, что понимаю о чем ты. /help',
            'Как то не разборчиво, может попробуешь /help?',
            'Эмм... что? /help',
            'Лучший способ общения со мной - команды. Начни с /help',
            'Я бездушная машина (пока что), поэтому лучше используй команды /help',
            'Кажется это что-то на человеческом... /help'
        }
        return random.choice(tuple(answer_set))
    bot.send_message(chat_id=update.message.chat_id,
                     text=random_answer())


def privet(bot, update):
    def say_privet():
        privet_set = {
            'И тебе привет, {})',
            'Hello, {}',
            'Здравствуйте, {})'
        }
        return random.choice(tuple(privet_set))
    bot.send_message(chat_id=update.message.chat_id,
                         text=say_privet().format(update.message.from_user.first_name))


def tabbbble(bot, job):
    Tabloid.paint_table()


bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token)
jo = updater.job_queue

jo.run_repeating(tabbbble, interval=60*2, first=0)

privethandler = MessageHandler(Filters.regex(r'(^\b(?i)привет$\b)|(^\b(?i)хай\b$)|(^\b(?i)здорова\b$)|(^\b(?i)здоров\b$)|(^\b(?i)даров\b$)'), privet)
updater.dispatcher.add_handler(privethandler)# Хэндлер приветствия
Whatyousay_handler = MessageHandler(Filters.text, What_you_say)
updater.dispatcher.add_handler(Whatyousay_handler)# Хэндлер что ты сказал?
updater.dispatcher.add_handler(CommandHandler('tth', tth))# Хэндлер tth
updater.dispatcher.add_handler(CommandHandler('Next', Next))# Хэндлер следующей игры
updater.dispatcher.add_handler(CommandHandler('Table', Table))# Хэндлер таблицы АПЛ
updater.dispatcher.add_handler(CommandHandler('Help', Help))# Хэндлер списка команд
updater.dispatcher.add_handler(CommandHandler('Welcome', Welcome))# Хэндлер повторения

updater.start_polling()
updater.idle()