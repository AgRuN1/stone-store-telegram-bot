from re import match

def simplify_article(article):
	return article.replace('-', '').replace(' ', '').lower()

def simplify_amount(amount_str):
	EPS = 0.001
	amount_str = amount_str.replace(',', '.')
	if '.' in amount_str:
		amount = float(amount_str)
		if amount - int(amount) < EPS:
			return int(amount)
		else:
			return amount
	return int(amount_str)

def check_phone(phone):
	digit_count = 0
	for c in phone:
		if c.isdigit():
			digit_count += 1
	return digit_count >= 10

def load_data(message):
	pass