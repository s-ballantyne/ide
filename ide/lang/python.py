from .language import Language


class Python(Language, name="Python", extensions=[".py"]):
	@staticmethod
	def lexer():
		pass

	@staticmethod
	def parser():
		pass
