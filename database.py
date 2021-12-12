import sqlite3
from datetime import datetime

class Database:
	lock = Lock()

	def __init__(self):
		self.__connection = sqlite3.connect('database.db')
		self._cursor = self.__connection.cursor()

	def save(self):
		self.__connection.commit()

	def __del__(self):
		self.__connection.close()

	def execute(self, sql, params=0):
		sql = sql.format(self._table)
		if params:
			self._cursor.execute(sql, params)
		else:
			self._cursor.execute(sql)

	def clear(self):
		sql = 'DELETE FROM {}'
		self.execute(sql)

class Stone:
	def __init__(self, row):
		self.type = row[0]
		self.city = row[1]
		self.mark = row[2]
		self.article = row[3]
		self.name = row[4]
		self.multipl = row[5]
		self.amount = row[6]
		self.coming = row[7]
		self.photo = row[8]
		self.article_name = row[9]

	def check_amount(self, amount):
		return amount <= self.amount

	def get_full_name(self):
		return '{} {} {}'.format(self.mark, self.article_name, self.name)

class Stones(Database):
	_table = 'stones'

	def get_list(self, name):
		sql = 'SELECT %s FROM {} GROUP BY %s' % (name, name)
		self.execute(sql)
		for row in self._cursor.fetchall():
			yield row[0]

	def get_stone(self, id):
		sql = 'SELECT * FROM {} WHERE id=?'
		self.execute(sql, (id,))
		res = self._cursor.fetchone()
		if res:
			return Stone(res)
		return False

	def find_stone(self, article='', city='', **kwargs):
		sql = 'SELECT * FROM {} WHERE article=? AND city=?'
		self.execute(sql, (article, city))
		res = self._cursor.fetchone()
		if res:
			return Stone(res)
		return False

	def append(self, row):
		sql = 'INSERT INTO {}(id, type, city, mark, article, name, multipl, amount, coming, photo, article_name) '
		sql += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
		params = (
			row['id'],
			row['type_name'],
			row['city'],
			row['mark'],
			row['article'],
			row['name'],
			row['multipl'],
			row['amount'],
			row['coming'],
			row['photo'],
			row['article_name']
		)
		self.execute(sql, params)


class Analog:
	def __init__(self, row):
		self.mark = row[0]
		self.article = row[1]
		self.name = row[2]
		self.stone_id = row[3]

class Analogs(Database):
	_table = 'analogs'

	def get_brands(self, type_name='', **kwargs):
		sql = 'SELECT a.mark FROM {} a INNER JOIN `stones` s ON a.stone_id = s.id WHERE s.type=?'
		self.execute(sql, (type_name,))
		for row in self._cursor.fetchall():
			yield row[0]

	def find_by_name(self, name='', article='', type_name='', brand='', **kwargs):
		sql = 'SELECT a.mark, a.article, a.name, a.stone_id FROM {} a INNER JOIN `stones` s ON a.stone_id=s.id WHERE (a.article LIKE ? OR LOWER(a.name) LIKE ?) AND a.mark =? AND s.type=?'
		article_param = '%{}%'.format(article)
		name_param = '%{}%'.format(name)
		self.execute(sql, (article_param, name_param, brand, type_name))
		res = self._cursor.fetchone()
		if res:
			return Analog(res)
		return False

	def append(self, row):
		sql = 'INSERT INTO {}(mark, article, name, stone_id) '
		sql += 'VALUES(?, ?, ?, ?)'
		params = (
			row['mark'],
			row['article'],
			row['name'],
			row['stone_id']
		)
		self.execute(sql, params)