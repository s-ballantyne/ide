from PySide2.QtGui import QFont
from PySide2.QtWidgets import QPlainTextEdit

from .linenumberarea import LineNumberArea


class Editor(QPlainTextEdit):
	def __init__(self, parent = None):
		super().__init__(parent)

		self.setFont(QFont("DejaVu Sans Mono", 12))

		self.lineNumberArea = LineNumberArea(self)

	def setIndentationWidth(self, n_spaces: int):
		self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * n_spaces)
