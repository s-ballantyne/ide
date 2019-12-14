import logging

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QTabWidget

from .codeeditor import CodeEditor
from .imageviewer import ImageViewer

from .documents import Document, TextDocument, ImageDocument


class MainTabBar(QTabWidget):
	def __init__(self, parent):
		super().__init__(parent)

		self.logger = logging.getLogger(f"{__name__}<{str(self.parent() and self.parent().window_id or -1)}>")

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

		self.logger.debug(f"Created new tab at {index} ('{name}').")

		return widget

	def createEditor(self, name: str = "", index: int = -1):
		return self.createTab(CodeEditor(self), name, index, self.editorIcon)

	def createImageViewer(self, name: str = "", index: int = -1):
		return self.createTab(ImageViewer(self), name, index, self.imageIcon)

	def activeTab(self):
		return self.currentWidget()

	def closeActiveTab(self):
		self.closeTab(self.currentIndex())

	def closeTab(self, index: int):
		self.logger.debug(f"Closing tab at index {index} ('{self.tabText(index)}').")

		self.removeTab(index)
		self.createEditorIfNotExists()

	def openDocument(self, document):
		if isinstance(document, TextDocument):
			# todo: move: document.hasPath() and document.path().name or "???"
			editor = self.createEditor(document.path().name if document.hasPath() else "???")
			editor.setDocument(document)

			self.setCurrentWidget(editor)
		elif isinstance(document, ImageDocument):
			viewer = self.createImageViewer(document.path().name if document.hasPath() else "???")
			viewer.setDocument(document)

			self.setCurrentWidget(viewer)
		else:
			self.logger.error(f"Unable to open unsupported document type '{document.name}'.")
