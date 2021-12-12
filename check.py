from bot import Bot
from database import Stones
from store import Store
from menu import main_menu, create_menu, remove_menu, base_menu, menu_check
from helpers import check_phone, simplify_article, simplify_amount
from data import send

bot = Bot()

def checking(message):
	markup = create_menu(*Stones().get_list('city'), 'Вернуться в меню')
	text = 'Вы выбрали проверить наличие.\nВыберите ваш город.'
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, city_handler)

def article_select(message):
	city = Store().get_value(message.from_user.id, 'city')
	markup = create_menu('Вернуться в меню')
	text='Вы выбрали {}.\nВведите артикул в формате буквы и цифры(пробелы, дефисы и регистр не важны: например ST-101 или st101).'
	msg = bot.send_message(message.chat.id, text.format(city), reply_markup=markup)
	bot.register_next_step_handler(msg, article_handler)

@menu_check
def city_handler(message):
	city = message.text
	cities = list(Stones().get_list('city'))
	if city not in cities:
		text = 'Выберите один из доступных городов.'
		msg = bot.send_message(message.chat.id, text)
		bot.register_next_step_handler(msg, city_handler)

	Store().set_value(message.from_user.id, 'city', city)
	article_select(message)
	
def amount_select(message):
	markup = create_menu('Вернуться в меню')
	text = 'Введите количество\n(разделитель точка или запятая):'
	msg = bot.send_message(message.chat.id, text, reply_markup=markup)
	bot.register_next_step_handler(msg, amount_handler)

@menu_check
def article_handler(message):
	article = simplify_article(message.text)
	Store().set_value(message.from_user.id, 'article', article)
	amount_select(message)

@menu_check
def amount_handler(message):
	try:
		amount = simplify_amount(message.text)
	except ValueError:
		text = 'Введите корректное количество.\nЭто должно быть целое число или десятичная дробь.'
		msg = bot.send_message(message.chat.id, text)
		bot.register_next_step_handler(msg, amount_handler)
		return
	if amount <= 0:
		text = 'Введите положительное количество материала.'
		bot.send_message(message.chat.id, text)
		return amount_select(message)
	stone = Stones().find_stone(**Store().get_data(message.from_user.id))
	if stone:
		if amount % stone.multipl:
			amount = (int(amount / stone.multipl) + 1) * stone.multipl
			if amount - int(amount) == 0:
				amount = int(amount)
		if stone.photo:
			bot.send_photo(message.chat.id, stone.photo)
		text = stone.get_full_name()
		text += ' в количестве {}шт.'.format(amount)
		order = 'Забронировать {}шт.'.format(amount)
		markup = base_menu(order)
		if stone.check_amount(amount):
			text += ' есть на складе в г. {}.\nНажмите, чтобы забронировать:'.format(stone.city)
			msg = bot.send_message(message.chat.id, text, reply_markup=markup)
		else:
			text += ' отсутствует на складе в г. {}.\nОжидаемая дата прихода: {}\n'.format(stone.city, stone.coming)
			text += 'Забронируйте или проверьте наличие другого цвета:'
			msg = bot.send_message(message.chat.id, text, reply_markup=markup)
		order_text = '{} в количестве {}шт.'.format(stone.get_full_name(), amount)
		Store().set_value(message.from_user.id, 'order', order_text)
		bot.register_next_step_handler(msg, menu_handler)
	else:
		bot.send_message(message.chat.id, 'Результат не найден')
		article_select(message)

def menu(message):
	txt = message.text
	if txt == 'Вернуться в меню':
		main_menu(message)
		return True
	elif txt == 'Изменить количество листов':
		amount_select(message)
		return True
	elif txt == 'Проверить другой цвет':
		article_select(message)
		return True
	return False

def menu_handler(message):
	if message.text.startswith('Забронировать'):
		order_handler(message)
	else:
		final_handler(message)

def order_handler(message):
	text = 'Введите ваш номер телефона.\nМенеджер свяжется в рабочее время.'
	msg = bot.send_message(message.chat.id, text, reply_markup=base_menu())
	bot.register_next_step_handler(msg, phone_handler)

def phone_handler(message):
	if not menu(message):
		phone = message.text
		if check_phone(phone):
			send(message)
			store = Store()
			order_text = store.get_value(message.from_user.id, 'order')
			text = '{} успешно зарезервирован.\nМенеджер сввяжется в рабочее время.'.format(order_text)
			msg = bot.send_message(message.chat.id, text, reply_markup=base_menu())
			bot.register_next_step_handler(msg, final_handler)
		else:
			text = 'Некорректный номер телефона.'
			bot.send_message(message.chat.id, text)
			order_handler(message)

def final_handler(message):
	if not menu(message):
		bot.send_message(message.chat.id, 'Команда не опознана.')
		main_menu(message)