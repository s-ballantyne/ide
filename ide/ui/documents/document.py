from PySide2.QtGui import QTextDocument


class Document(QTextDocument):
	def __init__(self, language):
		super().__init__()

		self._language = language

	def language(self):
		return self._language

	def setLanguage(self, language):
		self._language = language
