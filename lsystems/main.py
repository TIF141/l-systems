import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from lsystems.interface.gui import Window


basedir = os.path.dirname(__file__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "tree.ico")))
    window = Window()
    window.show()

    sys.exit(app.exec())
