from PySide2.QtGui import QPainter
from math import log10

from PySide2.QtWidgets import QWidget, QPlainTextEdit
from PySide2.QtCore import QSize, Qt

from ..colours import Black, White


class LineNumberArea(QWidget):
	def __init__(self, parent: QPlainTextEdit):
		super().__init__(parent)

		self.backgroundColour = Black
		self.numberColour = White
		self.numberAlignment = Qt.AlignCenter

	def numberWidth(self):
		block_count = self.parent().blockCount()
		digit_width = self.fontMetrics().horizontalAdvance("0")
		return 3 + digit_width * max(int(log10(block_count) + 1), 0)

	def sizeHint(self):
		return QSize(self.numberWidth(), 0)

	def paintEvent(self, event):
		width = self.width()
		font_height = self.fontMetrics().height()

		text_edit = self.parent()

		event_rect = event.rect()
		event_rect_top = event_rect.top()
		event_rect_bottom = event_rect.bottom()

		# Create painter
		painter = QPainter(self)

		# Background
		painter.fillRect(event_rect, self.backgroundColour)

		# Line numbers
		block = text_edit.firstVisibleBlock()
		block_number = block.blockNumber()

		top = int(text_edit.blockBoundingGeometry(block).translated(text_edit.contentOffset()).top())
		bottom = top + int(text_edit.blockBoundingRect(block).height())

		painter.setPen(self.numberColour)
		while block.isValid() and top <= event_rect_bottom:
			if block.isVisible() and bottom >= event_rect_top:
				painter.drawText(0, top, width, font_height, self.numberAlignment, str(block_number + 1))

			block = block.next()
			top = bottom
			bottom = top + int(text_edit.blockBoundingRect(block).height())
			block_number += 1
