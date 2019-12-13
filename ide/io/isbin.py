
# How can I detect is a file is binary (non-text) in Python?
# https://stackoverflow.com/a/7392391

_textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})


def is_binary_string(b: bytes):
	return bool(b.translate(None, _textchars))
