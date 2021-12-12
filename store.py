import pickle

class Store:
	__instance = None
	__datafile = 'store'

	def __new__(cls):
		if not isinstance(cls.__instance, Store):
			cls.__instance = super().__new__(cls)
			with open(cls.__datafile, 'rb') as f:
				 cls.__instance.__store = pickle.load(f)

		return cls.__instance

	def __save(self):
		with open(self.__datafile, 'wb') as f:
			pickle.dump(self.__store, f)

	def set_value(self, user_id, key, value):
		self.__store.setdefault(user_id, {})
		self.__store[user_id][key] = value
		self.__save()

	def get_value(self, user_id, key):
		return self.__store[user_id][key]
		
	def get_data(self, user_id):
		return self.__store[user_id]

	def clear(self, user_id):
		if user_id in self.__store:
			del self.__store[user_id]
			self.__save()