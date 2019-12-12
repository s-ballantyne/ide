from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QLabel


class ImageViewer(QLabel):
	def __init__(self, pixmap: QPixmap, parent):
		super().__init__(parent)
		self.setPixmap(pixmap)

		self.setAlignment(Qt.AlignCenter)
