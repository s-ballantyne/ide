from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel

from ..documents import ImageDocument


class ImageViewer(QLabel):
	def __init__(self, parent=None):
		super().__init__(parent)

		self._document = ImageDocument()

		self.setAlignment(Qt.AlignCenter)

	def document(self):
		return self._document

	def setDocument(self, document: ImageDocument):
		self._document = document
		self.setPixmap(document.pixmap())
