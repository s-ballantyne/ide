from PySide2.QtGui import QPixmap, Qt, QImageReader
from PySide2.QtWidgets import QLabel


supportedImageFormats = [f.data().decode("utf-8") for f in QImageReader.supportedImageFormats()]


class ImageViewer(QLabel):
	def __init__(self, pixmap: QPixmap, parent):
		super().__init__(parent)
		self.setPixmap(pixmap)

		self.setAlignment(Qt.AlignCenter)
