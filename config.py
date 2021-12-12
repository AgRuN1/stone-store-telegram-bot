from configparser import ConfigParser

class conf:
	__data = None
	def __new__(cls, section, key, type=str):
		if not isinstance(cls.__data, ConfigParser):
			cls.__data = ConfigParser()
			cls.__data.read('config.ini')

		try:
			return type(cls.__data[section][key])
		except KeyError:
			return False		