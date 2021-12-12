from bot import Bot
from store import Store
from config import conf
from helpers import simplify_article, simplify_amount
from database import Stones, Analogs
from menu import main_menu
from csv import reader

bot = Bot()

def stone_row(row):
	new_row = {}
	new_row['type_name'] = row[0]
	new_row['city'] = row[1]
	new_row['mark'] = row[2]
	new_row['article_name'] = row[3]
	new_row['article'] = simplify_article(row[3])
	new_row['name'] = row[4]
	new_row['multipl'] = simplify_amount(row[5])
	new_row['amount'] = simplify_amount((row[6]))
	new_row['coming'] = row[7]
	new_row['photo'] = row[8]
	new_row['id'] = row[9]
	return new_row

def analog_row(row):
	new_row = {}
	new_row['mark'] = row[0]
	new_row['article'] = simplify_article(row[1])
	new_row['name'] = row[2]
	new_row['stone_id'] = row[3]
	return new_row

def save(downloaded_file):
	data = reader(downloaded_file.decode().split('\n'))
	stones_data = []
	analogs_data = []
	is_header1 = True
	is_header2 = True
	for row in data:
		if len(row) == 4:
			if is_header1:
				is_header1 = False
			else:
				analogs_data.append(analog_row(row))
		elif len(row) == 10:
			if is_header2:
				is_header2 = False
			else:
				stones_data.append(stone_row(row))

	stones = Stones()
	stones.clear()
	for row in stones_data:
		stones.append(row)
	stones.save()

	analogs = Analogs()
	analogs.clear()
	for row in analogs_data:
		analogs.append(row)
	analogs.save()

def upload(message):
	if message.from_user.id != conf('bot', 'admin', type=int):
		text = 'Вы не можете выполнять эту команду'
		bot.send_message(message.chat.id, text)
		return main_menu(message)
	try:
		file_info = bot.get_file(message.document.file_id)
	except AttributeError:
		text = 'Загрузите файл для использования этой команды'
		bot.send_message(message.chat.id, text)
		return main_menu(message)
	downloaded_file = bot.download_file(file_info.file_path)
	try:
		save(downloaded_file)
	except Exception as e:
		bot.send_message(message.chat.id, str(e))
	else:
		text = 'Успешно загружено'
		bot.send_message(message.chat.id, text)
	finally:
		main_menu(message)

def send(message):
	phone = message.text
	text = '{} - {}'.format(phone, Store().get_value(message.from_user.id, 'order'))
	bot.send_message(conf('bot', 'admin'), text)