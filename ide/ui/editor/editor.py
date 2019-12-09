from PySide2.QtCore import QRect
from PySide2.QtGui import QFont, QResizeEvent
from PySide2.QtWidgets import QPlainTextEdit

from .linenumberarea import LineNumberArea


class Editor(QPlainTextEdit):
	def __init__(self, parent = None):
		super().__init__(parent)

		self.setFont(QFont("DejaVu Sans Mono", 12))

		self.lineNumberArea = LineNumberArea(self)
		self.setViewportMargins(self.lineNumberArea.numberWidth(), 0, 0, 0)

		self.blockCountChanged.connect(lambda: self.setViewportMargins(self.lineNumberArea.numberWidth(), 0, 0, 0))
		self.updateRequest.connect(self.updateLineNumberArea)

	def setIndentationWidth(self, n_spaces: int):
		self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * n_spaces)

	def resizeEvent(self, event: QResizeEvent):
		super().resizeEvent(event)

		# todo: move this into LineNumberArea
		cr = self.contentsRect()
		self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.lineNumberArea.numberWidth(), cr.height())

	def updateLineNumberArea(self, rect: QRect, dy: int = 0):
		# todo: move this into LineNumberArea
		if dy:
			self.lineNumberArea.scroll(0, dy)
		else:
			self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

		if rect.contains(self.viewport().rect()):
			self.setViewportMargins(self.lineNumberArea.numberWidth(), 0, 0, 0)

