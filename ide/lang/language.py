import logging
from typing import Iterable
from abc import abstractmethod


languages = {}
language_extensions = []

logger = logging.getLogger(__name__)


class Language:
	def __init__(self):
		pass

	def __init_subclass__(cls, name: str, extensions: Iterable[str], **kwargs):
		super().__init_subclass__(**kwargs)

		cls.name = name
		cls.extensions = extensions

		if name.lower() not in languages:
			logger.debug(f"Registered language '{name}' with extensions {', '.join(map(repr, extensions))}.")
			languages[name.lower()] = cls
			language_extensions.extend(extensions)
		else:
			logger.error(f"Conflict with languages: '{name}' already exists in registry.")


	@staticmethod
	@abstractmethod
	def lexer():
		pass

	@staticmethod
	@abstractmethod
	def parser():
		pass
