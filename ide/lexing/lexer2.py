import re

from .token import TokenType, Token


class LexerContext:
	def __init__(self):
		self._rules = []
		self._flags = re.MULTILINE
		self._regex = None

	@property
	def rules(self):
		return self._rules

	@property
	def flags(self):
		return self._flags

	def add_flag(self, flag: re.RegexFlag):
		self._flags |= flag

	@property
	def regex(self):
		if self._regex is None:
			self.compile()

		return self._regex

	def compile(self):
		parts = ["(?P<{}{}>{})".format(rule[0].name, i + 1, rule[1]) for i, rule in enumerate(self.rules)]
		self._regex = re.compile("|".join(parts))

	def add_pattern(self, token_type: TokenType, rule: str):
		self.rules.append((token_type, rule))

	def add_patterns(self, token_type: TokenType, *patterns):
		for pattern in patterns:
			self.rules.append((token_type, pattern))


class Lexer:
	def __init__(self, context: LexerContext, text: str, start_pos: int = 0):
		self._context = context
		self._text = text
		self._position = start_pos

	@property
	def context(self):
		return self._context

	@property
	def text(self):
		return self._text

	@property
	def position(self):
		return self._position

	@property
	def length(self):
		return len(self.text)

	def is_eof(self):
		return self.position >= self.length

	def next_token(self):
		if self.is_eof():
			return None

		match = self.context.regex.match(self.text, self.position)
		if match and match.end() > match.start():
			last_group = match.lastgroup

			token_type = TokenType[last_group[:-len(str(match.lastindex))]]
			text = match.group(last_group)

			token = Token(text, token_type, match.start(), match.end())
			token.match = match

			self._position = match.end()
			return token

		start_pos = self._position
		self._position += 1
		end_pos = self._position

		return Token(self.text[start_pos], TokenType.Unknown, start_pos, end_pos)

	def tokens(self):
		token = self.next_token()
		while token:
			yield token
			token = self.next_token()

