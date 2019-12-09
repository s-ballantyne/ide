from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QTabWidget

from .editor import Editor


class EditorTabBar(QTabWidget):
	def __init__(self, parent):
		super().__init__(parent)

		self.editorIcon = QIcon("icons/script_edit.png")

		self.setTabsClosable(True)
		self.tabCloseRequested.connect(self.closeEditor)

	def createEditorIfNotExists(self):
		if self.count() < 1:
			self.createEditor()

	def createEditor(self, name: str = "", index: int = -1):
		if not name:
			name = f"new {self.count() + 1}"

		index = min(self.count(), index)
		if index < 0:
			self.addTab(Editor(self), self.editorIcon, name)
		else:
			self.insertTab(index, Editor(self), self.editorIcon, name)

		if self.parent().logger:
			self.parent().logger.debug(f"Created new tab at {index} ('{name}').")

	def activeEditor(self):
		return self.currentWidget()

	def closeActiveEditor(self):
		self.closeEditor(self.currentIndex())

	def closeEditor(self, index: int):
		if self.parent().logger:
			self.parent().logger.debug(f"Closing tab at index {index} ('{self.tabText(index)}').")

		self.removeTab(index)
		self.createEditorIfNotExists()
