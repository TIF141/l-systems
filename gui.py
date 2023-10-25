import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from dataclasses import dataclass

# from PyQt6
from lsystems.generator import Generator
from lsystems.lsys import Lsys


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

    def initWindow(self):
        # super().__init__()
        self.setWindowTitle("window title")
        self.setGeometry(200, 500, 400, 300)
        # MainWindow.resize(422, 255)
        # self.centralwidget = QWidget(MainWindow)
        # self.createGridLayout()

        # self.createGridLayout()

        # # Want an example that lets you add an lsystem and add its rules
        self.addLSysButton = QPushButton("word1")
        # # self.addLSysButton.setGeometry(QtCore.QRect(160, 130, 93, 28))

        self.generateButton = QPushButton("word2")
        # # self.generateButton.setGeometry(QtCore.QRect(160, 110, 93, 28))

        self.label = QLabel()
        # # self.label.setGeometry(QtCore.QRect(220, 40, 201, 111))

        self.label.setText("")

        # MainWindow.setCentralWidget(self.centralwidget)
        # MainWindow.setWindowTitle("example title")
        self.addLSysButton.setText("button")
        self.addLSysButton.clicked.connect(self.get_input)
        self.generateButton.setText("generate")
        self.generateButton.clicked.connect(self.generate)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.show_button = QPushButton("Show")
        # self.show_button.clicked.connect(self.openSecondDialog)
        self.show_button.clicked.connect(self.showOnLabel)

        # vbox = QVBoxLayout(self)
        # vbox.addWidget(self.addLSysButton)
        # vbox.addWidget(self.generateButton)
        # vbox.addWidget(self.show_button)
        self.createGridLayout()
        self.show()

        self.data = Data()

    def createGridLayout(self):
        # self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        # layout.setColumnStretch(1, 4)
        # layout.setColumnStretch(2, 4)

        layout.addWidget(self.label, 0, 0, 3, 1)
        layout.addWidget(self.addLSysButton, 0, 1)
        layout.addWidget(self.generateButton, 1, 1)
        layout.addWidget(self.show_button, 2, 1)

        layout.setColumnStretch(0, 4)

        self.setLayout(layout)

    def openSecondDialog(self):
        dialog = Dialog(self)
        dialog.show()

    def get_input(self):
        key, done1 = QInputDialog.getText(self, "Input Dialog", "Enter rule key:")

        rule, done2 = QInputDialog.getText(self, "Input dialog2", "Enter rule item:")

        if done1 and done2:
            self.data.add_rule(key, rule)
            self.update_label()
            # self.addLSysButton.hide()

    def update_label(self):
        s = "\n".join(str(r) + " -> " + str(k) for r, k in self.data.rules.items())
        self.label.setText("Rules:\n" + s)

    def generate(self):
        assert self.data.rules is not {}
        lsys = Lsys(self.data.alphabet, self.data.rules)
        g = Generator(lsys, "F-F-F-F", 3)
        steps, history = g.generate_tortoise()
        from lsystems.draw import draw_coords

        from PIL import Image

        im = draw_coords(history, 200)
        im.save("image.jpg")

        # self.img = QPixmap("./image.jpg")
        # self.label = QLabel()
        # self.label.setPixmap(self.img)

        # self.grid = QGridLayout()
        # self.grid.addWidget(self.label, 1, 1)
        # self.setLayout(self.grid)

        # app = QApplication(sys.argv)
        # ex = Example()
        # app.exec()

    def showOnLabel(self):
        pixmap = QPixmap("image.jpg")
        self.label.setPixmap(pixmap)


class Data:
    def __init__(self):
        self.rules = {}

        self.alphabet = ["F", "f", "+", "-"]

    def add_rule(self, key, value):
        self.rules[key] = value


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_lbl = QLabel()
        lay = QVBoxLayout(self)

        lay.addWidget(self.image_lbl)
        self.load_image()

    def load_image(self):
        image_path = "./image.jpg"
        if image_path:
            pixmap = QPixmap(image_path)
            self.image_lbl.setPixmap(QPixmap(pixmap))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
