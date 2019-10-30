from enum import IntEnum

from .token import Token


class KeywordType(IntEnum):
	Unknown = 0

	# if, else, for, switch, ..
	ControlFlow = 1

	# inline, public, const, ..
	Qualifier = 2

	# int, double, union, struct, ..
	DataType = 3

	# bitand, or, sizeof, alignof, ..
	Operator = 4

	# Constants
	Constant = 5


class Keyword:
	def __init__(self, name, version = 0, deprecated = False):

		self._name = ""
		self._version = 0

		self._deprecated = False

	@property
	def name(self):
		return self._name

	@property
	def version(self):
		return self._version

	@property
	def deprecated(self) -> bool:
		return self._deprecated


class KeywordTable:
	def __init__(self, keywords: dict = None):
		if keywords is None:
			keywords = {}

		self._keywords = keywords

	@property
	def keywords(self):
		return self._keywords

	def copy(self):
		return KeywordTable(self.keywords.copy())

	def classify(self, token: Token):
		pass

