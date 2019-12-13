from typing import Iterable
from abc import abstractmethod


languages = {}


class Language:
	def __init__(self):
		pass

	def __init_subclass__(cls, name: str, extensions: Iterable[str], **kwargs):
		super().__init_subclass__(**kwargs)

		cls.name = name
		cls.extensions = extensions

		if name.lower() in languages:
			languages[name.lower()] = cls

	@staticmethod
	@abstractmethod
	def lexer():
		pass

	@staticmethod
	@abstractmethod
	def parser():
		pass
