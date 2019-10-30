from enum import IntEnum

from ide.string import escape_ex


class TokenType(IntEnum):
	Unknown = 0

	Whitespace = 10
	Newline = 11

	String = 20
	Number = 21

	Identifier = 30

	Operator = 40
	Separator = 41

	Comment = 50
	Preprocessor = 51


class Token:
	def __init__(self,	value: str, token_type: TokenType = TokenType.Unknown,
						start_pos: int = 0, end_pos: int = 0):
		self._value = value
		self._type = token_type
		self._start_pos = start_pos
		self._end_pos = end_pos

	def copy(self):
		return Token(self.value, self.type, self._start_pos, self.end_pos)

	@property
	def value(self) -> str:
		return self._value

	@property
	def escaped_value(self) -> str:
		return escape_ex(self.value)

	@property
	def type(self) -> TokenType:
		return self._type

	@property
	def start_pos(self) -> int:
		return self._start_pos

	@property
	def end_pos(self) -> int:
		return self._end_pos

	def __repr__(self):
		return f"{self.start_pos:0=4d}-{self.end_pos:0=4d} {self.type.name.lower()}: \"{self.escaped_value}\""
