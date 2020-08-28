import logging
from pathlib import Path

import requests

from PySide2.QtGui import QCloseEvent, QIcon, QKeySequence, QPixmap
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog
from PySide2.QtWidgets import QInputDialog, QLineEdit, QApplication

from ide.io import is_binary_string

from .util import centralisedRect
from .maintabbar import MainTabBar

from .documents import Document, TextDocument
from .documents import CodeDocument, ImageDocument, BinaryDocument

from .imageviewer import ImageViewer
from .codeeditor import CodeEditor


class IdeWindow(QMainWindow):
	next_window_id = 1

	def __init__(self):
		super().__init__()

		self.window_id = self.next_window_id
		self.next_window_id += 1

		self.logger = logging.getLogger(f"{__name__}<{self.window_id}>")
		self.logger.debug("Window created.")

		self.fileMenu = None
		self.aboutMenu = None
		self.createActions()

		self.tabs = MainTabBar(self)
		self.tabs.createEditorIfNotExists()

		self.setCentralWidget(self.tabs)
		self.setWindowTitle(f"IDE <{self.window_id}>" if self.window_id > 1 else "IDE")
		self.setWindowIcon(QIcon("icons/script_edit.png"))

		self.setGeometry(centralisedRect(qApp.desktop().availableGeometry()))

	def createActions(self):
		self.fileMenu = self.menuBar().addMenu("File")

		new_action = QAction("New", self.fileMenu)
		new_action.setStatusTip("Create a new file")
		new_action.setShortcut(QKeySequence.New)
		new_action.triggered.connect(self.newFile)
		self.fileMenu.addAction(new_action)

		close_action = QAction("Close", self.fileMenu)
		close_action.setStatusTip("Closes current tab")
		close_action.setShortcut(QKeySequence.Close)
		close_action.triggered.connect(self.closeFile)
		self.fileMenu.addAction(close_action)

		open_action = QAction("Open", self.fileMenu)
		open_action.setStatusTip("Open a file")
		open_action.setShortcut(QKeySequence.Open)
		open_action.triggered.connect(self.openFileWithDialog)
		self.fileMenu.addAction(open_action)

		open_from_url_action = QAction("Open from URL", self.fileMenu)
		open_from_url_action.setStatusTip("Open a file from a URL")
		open_from_url_action.triggered.connect(self.openFileFromUrlWithDialog)
		self.fileMenu.addAction(open_from_url_action)

		self.fileMenu.addSeparator()

		rename_action = QAction("Rename", self.fileMenu)
		rename_action.setStatusTip("Rename currently open file")
		rename_action.triggered.connect(self.renameFileWithDialog)
		self.fileMenu.addAction(rename_action)

		self.fileMenu.addSeparator()

		save_action = QAction("Save", self.fileMenu)
		save_action.setStatusTip("Save a file")
		save_action.setShortcut(QKeySequence.Save)
		save_action.triggered.connect(self.saveFile)
		self.fileMenu.addAction(save_action)

		save_as_action = QAction("Save as", self.fileMenu)
		save_as_action.setStatusTip("Save a file somewhere else")
		save_as_action.setShortcut(QKeySequence.SaveAs)
		save_as_action.triggered.connect(self.saveFileAsWithDialog)
		self.fileMenu.addAction(save_as_action)

		save_all_action = QAction("Save all", self.fileMenu)
		save_all_action.setStatusTip("Save all files")
		save_all_action.triggered.connect(self.saveAllFiles)
		self.fileMenu.addAction(save_all_action)

		self.fileMenu.addSeparator()

		quit_action = QAction("Quit", self.fileMenu)
		quit_action.setStatusTip("Quit the application")
		quit_action.setShortcut(QKeySequence.Quit)
		quit_action.triggered.connect(self.close)
		self.fileMenu.addAction(quit_action)

		self.aboutMenu = self.menuBar().addMenu("About")

		about_qt_action = QAction("About Qt", self.aboutMenu)
		about_qt_action.setStatusTip("Show Qt for Python's about box")
		about_qt_action.triggered.connect(qApp.aboutQt)
		self.aboutMenu.addAction(about_qt_action)

	def newFile(self):
		self.logger.debug("New file requested.")
		self.tabs.createEditor()

	def closeFile(self):
		self.logger.debug("Close active tab requested.")
		self.tabs.closeActiveTab()

	def openFile(self, path: str):
		path = Path(path)
		self.logger.debug(f"Attempting to open file at '{path}'...")

		if path.is_file():
			document_class = Document.detectTypeFromName(path.name)
			if not document_class:
				self.logger.warning(f"Failed to recognise file type from name for '{path}', checking contents...")

				with path.open("rb") as f:
					document_class = Document.detectTypeFromSample(f.read(1024))

			# todo: mimetypes

			if not document_class:
				self.logger.error(f"Could not recognise file type for '{path}'.")
			else:
				self.logger.debug(f"File at '{path}' appears to have type '{document_class.name}'.")

				document = document_class(path)
				document.reload()
				self.tabs.openDocument(document)

		else:
			self.logger.error(f"Attempted to open non-file at '{path}'.")

	def openFileWithDialog(self):
		self.logger.debug("Opening file dialog...")

		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setViewMode(QFileDialog.Detail)

		if dialog.exec():
			for file in dialog.selectedFiles():
				self.openFile(file)

	def openFileFromUrl(self, url: str):
		self.logger.debug(f"Attempting to open URL at '{url}'...")

		try:
			r = requests.get(url)

			self.logger.info(f"Request to '{url}': got response, status: {r.status_code}, time taken: {r.elapsed}.")
			self.logger.debug(f"Response headers: {r.headers}")
		except ConnectionError as e:
			self.logger.warning(f"Request to '{url}': connection failed.")
			self.logger.warning(e)
		except TimeoutError as e:
			self.logger.warning(f"Request to '{url}': timed out.")
			self.logger.warning(e)

		if r.status_code == requests.codes.ok:
			editor = self.tabs.createEditor(url.rsplit("/", 1)[-1] + " (URL)")
			editor.setPlainText(r.text)

			self.tabs.setCurrentWidget(editor)
		else:
			self.logger.error(f"Request to '{url}': received non-ok status code {r.status_code}.")

	def openFileFromUrlWithDialog(self):
		text =\
		"""
		Use raw URLs only.
		
		Some useful URLs:
		 - https://pastebin.com/raw/<id>
		 - https://raw.githubusercontent.com/<user>/<repo>/master/<path>
		"""

		self.logger.debug("Opening URL dialog...")
		text, ok = QInputDialog.getText(self, "Open a URL", text, QLineEdit.Normal, "https://raw.githubusercontent.com/<user>/<repo>/master/<file>")

		if ok and text:
			self.openFileFromUrl(text)

	def renameFile(self, name: str):
		pass

	def renameFileWithDialog(self):
		pass

	def saveFile(self):
		self.logger.debug("Attempting to save current tab...")

		if self.tabs.activeTab() is CodeEditor:
			self.tabs.activeTab().document().save()

	def saveAllFiles(self):
		for i in range(self.tabs.count()):
			tab = self.tabs.widget(i)
			if tab is CodeEditor:
				tab.document().save()

	def saveFileAs(self):
		pass

	def saveFileAsWithDialog(self):
		pass

	def closeEvent(self, event: QCloseEvent):
		self.logger.debug("Close event accepted.")
		event.accept()
