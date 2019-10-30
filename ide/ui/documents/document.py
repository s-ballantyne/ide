from typing import Iterable

from PySide2.QtGui import QTextDocument


class Document(QTextDocument):
	documents = {}

	def __init__(self):
		super().__init__()

	def __init_subclass__(cls, name: str, extensions: Iterable[str], **kwargs):
		super().__init_subclass__(cls, **kwargs)
