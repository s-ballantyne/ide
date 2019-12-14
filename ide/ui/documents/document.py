import logging
from pathlib import PurePath, Path
from abc import abstractmethod

from PySide2.QtGui import QImageReader, QPixmap, QTextDocument

from ide.io import is_binary_string
from ide.lang import language_extensions


documents = {}
logger = logging.getLogger(__name__)


class Document:
	def __init__(self, path=None):
		self._path = path

	def __init_subclass__(cls, name: str, **kwargs):
		super().__init_subclass__(**kwargs)

		cls.name = name

		if name.lower() not in documents:
			logger.debug(f"Registered document type '{name}'.")
			documents[name.lower()] = cls
		else:
			logger.error(f"Conflict with document types: '{name}' already exists in registry.")

	def path(self):
		return self._path

	def setPath(self, path):
		self._path = path

	def hasPath(self):
		return isinstance(self._path, Path)

	def canSave(self):
		return self.hasPath() and self._path.is_file()

	@staticmethod
	def detectTypeFromName(name: str):
		for document in documents.values():
			if document.detectTypeFromName(name):
				return document

	@staticmethod
	def detectTypeFromSample(sample):
		for document in documents.values():
			if document.detectTypeFromSample(sample):
				return document

	@abstractmethod
	def reload(self):
		pass


class TextDocument(Document, name="Text"):
	def __init__(self, path=None):
		super().__init__(path)

		self._document = QTextDocument()

	def document(self):
		return self._document

	@staticmethod
	def detectTypeFromName(name: str):
		return PurePath(name).suffix in [".txt", ".log"]

	@staticmethod
	def detectTypeFromSample(sample):
		try:
			sample.decode()
		except (UnicodeDecodeError, AttributeError):
			return False

		return True

	def reload(self):
		with self.path().open("r") as f:
			self._document.setPlainText(f.read())


class CodeDocument(TextDocument, name="Source Code"):
	def __init__(self, path=None):
		super().__init__(path)

		self._language = None

	def language(self):
		return self._language

	def setLanguage(self, language):
		self._language = language

	@staticmethod
	def detectTypeFromName(name: str):
		return PurePath(name).suffix in language_extensions


class ImageDocument(Document, name="Image"):
	extensions = ["." + f.data().decode("utf-8") for f in QImageReader.supportedImageFormats()]

	def __init__(self, path=None):
		super().__init__(path)

		self._pixmap = QPixmap(str(path)) if path else QPixmap()

	def pixmap(self):
		return self._pixmap

	def setPixmap(self, pixmap):
		self._pixmap = pixmap

	@staticmethod
	def detectTypeFromName(name: str):
		return PurePath(name).suffix in ImageDocument.extensions

	@staticmethod
	def detectTypeFromSample(sample):
		return False

	def reload(self):
		self._pixmap = QPixmap(str(self.path()))


class BinaryDocument(Document, name="Binary"):
	def __init__(self, path=None):
		super().__init__(path)

		self._data = b""

	@staticmethod
	def detectTypeFromName(name):
		return PurePath(name).suffix in [".exe", ".dll", ".so", ".bin"]

	@staticmethod
	def detectTypeFromSample(sample):
		return is_binary_string(sample)

	def reload(self):
		with self.path().open("rb") as f:
			self._data = f.read()
