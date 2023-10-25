import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QImage

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

        self.addRuleButton = QPushButton()
        self.addRuleButton.setText("Add rule")
        self.addRuleButton.clicked.connect(self.get_new_rule)

        self.rulesList = QListWidget()
        self.rulesList.addItems([])
        # self.rulesList.currentItemChanged.connect(self.generate)

        self.iterations = QSpinBox()
        self.iterations.setMinimum(0)
        # self.iterations.valueChanged.connect(self.generate)

        self.generateButton = QPushButton()
        self.generateButton.setText("Generate")
        self.generateButton.clicked.connect(self.generate)
        # self.rulesList.current

        # self.addLSysButton = QPushButton()

        # self.generateButton = QPushButton()

        self.label = QLabel()

        self.label.setText("")
        # self.addLSysButton.setText("button")
        # self.addLSysButton.clicked.connect(self.get_input)
        # self.generateButton.setText("generate")
        # self.generateButton.clicked.connect(self.generate)

        # self.show_button = QPushButton("Show")
        # self.show_button.clicked.connect(self.showOnLabel)

        self.createGridLayout()
        self.show()

        self.data = Data()

    def createGridLayout(self):
        layout = QGridLayout()

        layout.addWidget(self.label, 0, 0, 1, 1)
        layout.addWidget(self.addRuleButton, 0, 1, 1, 1)
        layout.addWidget(self.rulesList, 1, 1, 1, 1)
        layout.addWidget(self.iterations, 2, 1, 1, 1)
        layout.addWidget(self.generateButton, 3, 1, 1, 1)
        # layout.addWidget(self.addLSysButton, 0, 1)
        # layout.addWidget(self.generateButton, 1, 1)
        # layout.addWidget(self.show_button, 2, 1)

        layout.setColumnStretch(0, 4)

        self.setLayout(layout)

    def openSecondDialog(self):
        dialog = Dialog(self)
        dialog.show()

    def get_new_rule(self):
        rule_entry = InputDialog(self)
        rule_entry.exec()
        key = rule_entry.keyEntry.text()
        value = rule_entry.valueEntry.text()
        self.data.add_rule(key, value)

        rule_str = key + " -> " + value
        self.rulesList.addItem(rule_str)

    def get_input(self):
        key, done1 = QInputDialog.getText(self, "Input Dialog", "Enter rule key:")

        rule, done2 = QInputDialog.getText(self, "Input dialog2", "Enter rule item:")

        if done1 and done2:
            self.data.add_rule(key, rule)
            self.update_label()

    def update_label(self):
        s = "\n".join(str(r) + " -> " + str(k) for r, k in self.data.rules.items())
        self.label.setText("Rules:\n" + s)

    def generate(self):
        assert self.data.rules is not {}
        lsys = Lsys(self.data.alphabet, self.data.rules)
        if int(self.iterations.value()) != 0:
            print("generating")
            g = Generator(lsys, "F-F-F-F", self.iterations.value())
            steps, history = g.generate_tortoise()
            from lsystems.draw import draw_coords

            im = draw_coords(history, 200).copy()
            # self.data.img = im
            qimage = QImage(
                im, im.shape[0], im.shape[1], QImage.Format.Format_Grayscale8
            )
            pixmap = QPixmap(qimage)
            self.label.setPixmap(pixmap)

    def showOnLabel(self):
        pixmap = QPixmap("image.jpg")
        self.label.setPixmap(pixmap)


class Data:
    def __init__(self):
        self.rules = {}

        self.alphabet = ["F", "f", "+", "-"]

    def add_rule(self, key, value):
        self.rules[key] = value


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data = parent.data
        self.createItems()
        self.generateLayout()

    def createItems(self):
        self.keyEntry = QLineEdit()
        self.keyEntry.setPlaceholderText("Enter rule key")

        self.valueEntry = QLineEdit()
        self.valueEntry.setPlaceholderText("Enter rule value")

        # self.iterationsEntry = QSpinBox()
        # self.iterationsEntry.setMinimum(0)

        self.buttons = QDialogButtonBox(self)
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # self.okButton = QPushButton()
        # self.okButton.setText("Create rule")
        # self.okButton.clicked.connect(self.add_rule)

    def generateLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.keyEntry)
        self.layout.addWidget(self.valueEntry)
        # self.layout.addWidget(self.iterationsEntry)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def add_rule(self):
        key = self.keyEntry.text
        val = self.valueEntry.text
        # iterations = self.iterationsEntry.value
        self.data.add_rule(key, val)
        self.close()


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = parent.data

        self.image_lbl = QLabel()
        lay = QVBoxLayout(self)

        lay.addWidget(self.image_lbl)
        self.load_image()

    def load_image(self):
        image = self.data.img
        if image_path:
            pixmap = QPixmap(image)
            self.image_lbl.setPixmap(QPixmap(pixmap))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
