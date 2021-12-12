from menu import main_menu, create_menu, remove_menu, menu_check
from store import Store
from bot import Bot
from helpers import simplify_article
from check import amount_select
from database import Stones, Analogs

bot = Bot()

def searching(message):
	types = Stones().get_list('type')
	markup = create_menu(*types, 'Вернуться в меню')
	text = 'Вы выбрали подобрать аналог.\nВыберите тип материала.'
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, type_handler)

def brand_select(message):
	brands = Analogs().get_brands(**Store().get_data(message.from_user.id))
	markup = create_menu(*brands, 'Вернуться в меню')
	text = 'Вы выбрали {}.Выберите бренд к которому подобрать аналог:'.format(message.text)
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, brand_handler)

@menu_check
def type_handler(message):
	stone_type = message.text
	types = list(Stones().get_list('type'))
	if stone_type not in types:
		text = 'Выберите один из данных типов.'
		bot.send_message(message.chat.id, text)
		return searching(message)
	Store().set_value(message.from_user.id, 'type_name', stone_type)
	brand_select(message)

@menu_check
def brand_handler(message):
	brand = message.text
	brands = list(Analogs().get_brands(**Store().get_data(message.from_user.id)))
	if brand not in brands:
		text = 'Выберите один из предложенных брендов.'
		bot.send_message(message.chat.id, text)
		brand_select(message)
	Store().set_value(message.from_user.id, 'brand', brand)
	text = 'Вы выбрали {}.'.format(brand)
	text += 'Введите артикул, название или их часть '
	text += '(пробелы, дефисы и регистр не важны: например, ST-101 или st101; Aurora grey и тд).'
	markup = create_menu('Вернуться в меню')
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, name_handler)

def city_select(message):
	cities = Stones().get_list('city')
	markup = create_menu(*cities, 'Вернуться в меню')
	order_name = Store().get_value(message.from_user.id, 'order')
	text = 'Аналог: {}\nХотите забронировать ?\nВыберите город склада'.format(order_name)
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, city_handler)

@menu_check
def name_handler(message):
	name = message.text.lower()
	article = simplify_article(name)
	store = Store()
	analog = Analogs().find_by_name(name=name, article=article, **store.get_data(message.chat.id))
	if analog:
		stone = Stones().get_stone(analog.stone_id)
		if stone.photo:
			bot.send_photo(message.chat.id, stone.photo)
		store.set_value(message.from_user.id, 'order', stone.get_full_name())
		store.set_value(message.from_user.id, 'city', stone.city)
		store.set_value(message.from_user.id, 'article', stone.article)
		city_select(message)
	else:
		text = 'Не удалось найти аналог по заданным параметрам.'
		bot.send_message(message.chat.id, text)
		main_menu(message)

@menu_check
def city_handler(message):
	city = message.text
	cities = list(Stones().get_list('city'))
	if city not in cities:
		text = 'Выберите один из предложенных городов.'
		bot.send_message(message.chat.id, text)
		city_select(message)
		return
	if Store().get_value(message.from_user.id, 'city') != city:
		text = 'В этом городе на складе данный товар отсутствует'
		bot.send_message(message.chat.id, text)
		main_menu(message)
	else:
		amount_select(message)