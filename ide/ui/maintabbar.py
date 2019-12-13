from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QTabWidget

from .codeeditor import Editor
from .imageviewer import ImageViewer


class MainTabBar(QTabWidget):
	def __init__(self, parent):
		super().__init__(parent)

		self.editorIcon = QIcon("icons/script_edit.png")
		self.imageIcon = QIcon("icons/image.png")

		self.setTabsClosable(True)
		self.tabCloseRequested.connect(self.closeTab)

	def createEditorIfNotExists(self):
		if self.count() < 1:
			return self.createEditor()

	def createTab(self, widget, name: str = "", index: int = -1, icon: QIcon = None):
		if not name:
			name = f"new {self.count() + 1}"

		index = min(self.count(), index)
		if index < 0:
			self.addTab(widget, icon, name)
		else:
			self.insertTab(index, widget, icon, name)

		if self.parent().logger:
			self.parent().logger.debug(f"Created new tab at {index} ('{name}').")

		return widget

	def createEditor(self, name: str = "", index: int = -1):
		return self.createTab(Editor(self), name, index, self.editorIcon)

	def createImageViewer(self, pixmap: QPixmap, name: str = "", index: int = -1):
		return self.createTab(ImageViewer(pixmap, self), name, index, self.imageIcon)

	def activeTab(self):
		return self.currentWidget()

	def closeActiveTab(self):
		self.closeTab(self.currentIndex())

	def closeTab(self, index: int):
		if self.parent().logger:
			self.parent().logger.debug(f"Closing tab at index {index} ('{self.tabText(index)}').")

		self.removeTab(index)
		self.createEditorIfNotExists()
