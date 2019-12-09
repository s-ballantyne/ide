import logging

from PySide2.QtCore import qApp
from PySide2.QtGui import QCloseEvent, QIcon, QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction

from .util import centralisedRect
from .editortabbar import EditorTabBar


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

		self.editors = EditorTabBar(self)
		self.editors.createEditorIfNotExists()

		self.setCentralWidget(self.editors)
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
		close_action.setStatusTip("Closes current editor tab")
		close_action.setShortcut(QKeySequence.Close)
		close_action.triggered.connect(self.closeFile)
		self.fileMenu.addAction(close_action)

		open_action = QAction("Open", self.fileMenu)
		open_action.setStatusTip("Open a file")
		open_action.setShortcut(QKeySequence.Open)
		open_action.triggered.connect(self.openFile)
		self.fileMenu.addAction(open_action)

		open_from_url_action = QAction("Open from URL", self.fileMenu)
		open_from_url_action.setStatusTip("Open a file from a URL")
		open_from_url_action.triggered.connect(self.openFileFromUrl)
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
		save_as_action.triggered.connect(self.saveFileAs)
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
		self.editors.createEditor()

	def closeFile(self):
		self.logger.debug("Close active editor requested.")
		self.editors.closeActiveEditor()

	def openFile(self):
		pass

	def openFileFromUrl(self):
		pass

	def saveFile(self):
		pass

	def saveAllFiles(self):
		pass

	def saveFileAs(self):
		pass

	def closeEvent(self, event: QCloseEvent):
		self.logger.debug("Close event accepted.")
		event.accept()
