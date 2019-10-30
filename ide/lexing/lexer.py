import re

from .token import TokenType, Token


class Matcher:
	def __init__(self, token_type: TokenType):
		self._token_type = token_type

	@property
	def token_type(self):
		return self._token_type

	def match(self, text: str, start_pos: int = 0):
		raise NotImplementedError


class ExactMatcher(Matcher):
	def __init__(self, token_type: TokenType, text: str):
		super().__init__(token_type=token_type)
		self._text = text

	@property
	def text(self):
		return self._text

	def match(self, text: str, start_pos: int = 0):
		substr = text[start_pos:start_pos+len(self.text)]
		if substr == self.text:
			return substr, start_pos + len(self.text)
		else:
			return "", start_pos


class PatternMatcher(Matcher):
	def __init__(self, token_type: TokenType, regex: str, flags: re.RegexFlag = re.MULTILINE):
		super().__init__(token_type=token_type)
		self._regex = re.compile(regex, flags)

	@property
	def regex(self):
		return self._regex

	def match(self, text: str, start_pos: int = 0):
		match = self.regex.match(text, start_pos)
		group = match.group() if match else ""
		end = match.end() if match else start_pos
		return group, end


class DynamicMatcher(Matcher):
	def __init__(self, token_type: TokenType, func: callable):
		super().__init__(token_type=token_type)
		self._callable = func

	@property
	def func(self):
		return self._callable

	def match(self, text: str, start_pos: int = 0):
		return self.func(text, start_pos)


class LexerContext:
	def __init__(self):
		self._matchers = []

	@property
	def matchers(self):
		return self._matchers

	def add_symbol(self, token_type: TokenType, text: str):
		self.matchers.append(ExactMatcher(token_type, text))

	def add_pattern(self, token_type: TokenType, pattern: str, flags: re.RegexFlag = re.MULTILINE):
		self.matchers.append(PatternMatcher(token_type, pattern, flags))

	def add_dynamic(self, token_type: TokenType, func: callable):
		self.matchers.append(DynamicMatcher(token_type, func))

	def add_symbols(self, token_type: TokenType, *texts):
		for text in texts:
			self.matchers.append(ExactMatcher(token_type, text))

	def add_patterns(self, token_type: TokenType, *patterns, flags: re.RegexFlag = 0):
		for pattern in patterns:
			self.matchers.append(PatternMatcher(token_type, pattern, flags))


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

		for matcher in self.context.matchers:
			text, end_pos = matcher.match(self.text, self.position)
			if end_pos > self.position:
				token = Token(text, matcher.token_type, self.position, end_pos)
				self._position = end_pos
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
