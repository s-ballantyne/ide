import logging
from pathlib import Path

import requests

from PySide2.QtCore import qApp
from PySide2.QtGui import QCloseEvent, QIcon, QKeySequence, QPixmap
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QInputDialog, QLineEdit

from ide.io import is_binary_string

from .util import centralisedRect
from .maintabbar import MainTabBar
from .imageviewer import supportedImageFormats


class IdeWindow(QMainWindow):
	next_window_id = 1

	def __init__(self):
		super().__init__()

		self.window_id = self.next_window_id
		self.next_window_id += 1

		self.logger = logging.getLogger(f"ide.IdeWindow<{self.window_id}>")
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
			if path.suffix and path.suffix.lower()[1:] in supportedImageFormats:
				self.tabs.setCurrentWidget(self.tabs.createImageViewer(QPixmap(str(path)), path.name))
			else:
				with path.open("rb") as f:
					is_binary = is_binary_string(f.read(1024))

					if is_binary:
						f.seek(0)

						# todo: implement hex editor
						self.logger.error(f"File '{path}' appears to be binary.")

				if not is_binary:
					with path.open() as f:
						editor = self.tabs.createEditor(path.name)
						editor.setPlainText(f.read())
						self.tabs.setCurrentWidget(editor)
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

	def saveFile(self):
		pass

	def saveAllFiles(self):
		pass

	def saveFileAs(self):
		pass

	def saveFileAsWithDialog(self):
		pass

	def closeEvent(self, event: QCloseEvent):
		self.logger.debug("Close event accepted.")
		event.accept()
