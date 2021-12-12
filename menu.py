from functools import wraps

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from store import Store
from bot import Bot

bot = Bot()

actions = {}

def setup_menu(current_actions):
	global actions
	actions = current_actions

def main_menu(message):
	Store().clear(message.from_user.id)
	current_actions = filter(lambda act: not act.startswith('admin:'), actions.keys())
	markup = create_menu(*current_actions, width=2)
	msg = bot.send_message(message.chat.id, 'Выберите что хотите сделать', reply_markup=markup)
	bot.register_next_step_handler(msg, action_handler)

def menu_check(func):
	@wraps(func)
	def wrapper(message):
		if message.text == 'Вернуться в меню':
			main_menu(message)
		else:
			func(message)
	return wrapper

def action_handler(message):
	if message.content_type == 'document':
		return actions['admin:upload'](message)
	try:
		actions[message.text](message)
	except KeyError:
		msg = bot.send_message(message.chat.id, 'Выберите одно из действий')
		main_menu(message)

def base_menu(*args):
	return create_menu(*args, 'Проверить другой цвет', 'Изменить количество листов', 'Вернуться в меню')

def create_menu(*args, width=1):
	markup = ReplyKeyboardMarkup(row_width=width, resize_keyboard=True)
	for arg in args:
		btn = KeyboardButton(arg)
		markup.add(btn)
	return markup

def remove_menu():
	return ReplyKeyboardRemove()
