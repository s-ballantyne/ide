import string


def escape_newlines(text: str):
	text = text.replace("\r", "\\r")
	text = text.replace("\n", "\\n")

	return text


def escape(text: str):
	text = text.replace("\\", "\\\\")
	text = text.replace("\t", "\\t")
	text = text.replace("\"", "\\\"")
	text = text.replace("\'", "\\\'")

	return escape_newlines(text)


printable = string.ascii_letters + string.digits + string.punctuation
def escape_ex(text: str):
	def _escape(c):
		if c in printable:
			return c
		elif c <= '\xff':
			return r"\x{0:02x}".format(ord(c))
		else:
			return c.encode("unicode_escape").decode("ascii")

	return "".join(_escape(c) for c in text)


def escape_np(text: str):
	def _escape(c):
		if c.isprintable():
			return c
		elif c <= '\xff':
			return r"\x{0:02x}".format(ord(c))
		else:
			return c.encode("unicode_escape").decode("ascii")

	return "".join(_escape(c) for c in text)
