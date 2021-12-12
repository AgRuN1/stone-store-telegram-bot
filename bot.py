import telebot

from config import conf

class Bot:
	__instance = None
	def __new__(cls):
		if not isinstance(cls.__instance, telebot.TeleBot):
			cls.__instance = telebot.TeleBot(conf('bot', 'token'))
		return cls.__instance