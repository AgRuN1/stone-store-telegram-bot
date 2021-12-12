import traceback

from bot import Bot
from menu import main_menu, setup_menu
from data import upload
from check import checking
from search import searching

bot = Bot()

actions = {
	'Проверить наличие.': checking,
	'Подобрать аналог': searching,
	'admin:upload': upload
}

@bot.message_handler(commands=['start'])
def start(message):
	main_menu(message)

@bot.message_handler(content_types=['text'])
def default(message):
	bot.send_message(message.from_user.id, 'Команда не опознана.')
	main_menu(message)

if __name__ == '__main__':
	bot.remove_webhook()
	bot.enable_save_next_step_handlers(delay=2)
	bot.load_next_step_handlers()

	setup_menu(actions)

	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as error:
			with open('log.error', 'a') as f:
				traceback.print_exception(type(error), error, error.__traceback__, file=f)
