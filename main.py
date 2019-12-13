#!/usr/bin/env python3
import os
import sys
import pathlib
import argparse
import logging

from PySide2.QtWidgets import QApplication

from ide.ui import IdeWindow


def setup_logger(log, log_level):
	formatter = logging.Formatter(
		"%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s: %(message)s", datefmt="%H:%M:%S"
	)

	stdout_handler = logging.StreamHandler()
	stdout_handler.setFormatter(formatter)
	log.addHandler(stdout_handler)

	log.setLevel(log_level)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Sets log level to debug")
	parser.add_argument("-d", "--dark", action="store_true", default=True, help="Toggles dark style.")
	parser.add_argument("files", nargs="*")

	args = parser.parse_args()

	# Logger
	logger = logging.getLogger("ide")
	setup_logger(logger, logging.DEBUG if args.verbose else logging.INFO)

	os.environ["QT_API"] = "PySide2"

	# Application
	app = QApplication(sys.argv)

	# Theme
	if args.dark:
		try:
			import qdarkstyle
		except ImportError as e:
			qdarkstyle = False

			logger.warning("Failed to import dark theme (QDarkStyle).")
			logger.warning(e)

		if qdarkstyle:
			app.setStyleSheet(qdarkstyle.load_stylesheet())

	# Create main IDE window
	ide_window = IdeWindow()
	ide_window.show()

	# Check command line for paths to load into the codeeditor
	for file_name in args.files:
		path = pathlib.Path(file_name)
		ide_window.openFile(path)

	# Application loop
	logger.debug("Entering main application loop..")
	code = app.exec_()

	if code == 0:
		logger.debug("Main application loop exited successfully.")
	else:
		logger.warning(f"Main application loop exited with non-zero exit code ({code})!")

	sys.exit(code)
else:
	raise ImportError("cannot import main, idiot")
