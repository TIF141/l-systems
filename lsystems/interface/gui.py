import sys
from PyQt6.QtGui import QPixmap, QImage

from PyQt6.QtWidgets import (
    QButtonGroup,
    QPushButton,
    QListWidget,
    QWidget,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QGridLayout,
    QApplication,
    QErrorMessage,
)
from lsystems.interface.input_dialogs import RuleInputDialog, AxiomInputDialog

from lsystems.generator import Generator
from lsystems.lsys import Lsys


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle("window title")
        self.setGeometry(200, 500, 400, 300)

        self.rulesButtons = QButtonGroup()
        self.addRuleButton = QPushButton()
        self.removeRuleButton = QPushButton()
        self.addRuleButton.setText("Add rule")
        self.removeRuleButton.setText("Remove rule")
        self.rulesButtons.addButton(self.addRuleButton)
        self.rulesButtons.addButton(self.removeRuleButton)
        self.addRuleButton.clicked.connect(self.get_new_rule)
        self.removeRuleButton.clicked.connect(self.remove_rule)

        self.rulesListTitle = QLabel(self)
        self.rulesListTitle.setText("Rules")

        self.rulesList = QListWidget(self)
        self.rulesList.addItems([])

        self.iterationsTitle = QLabel(self)
        self.iterationsTitle.setText("Iterations")

        self.iterations = QSpinBox(self)
        self.iterations.setMinimum(0)

        self.angleTitle = QLabel(self)
        self.angleTitle.setText("Branching angle")

        self.angle = QDoubleSpinBox(self)
        self.angle.setValue(90.0)

        self.axiomListTitle = QLabel(self)
        self.axiomListTitle.setText("Axioms")

        self.axiomsButtons = QButtonGroup()
        self.addAxiomButton = QPushButton()
        self.removeAxiomButton = QPushButton()
        self.addAxiomButton.setText("Add axiom")
        self.removeAxiomButton.setText("Remove axiom")
        self.axiomsButtons.addButton(self.addAxiomButton)
        self.axiomsButtons.addButton(self.removeAxiomButton)
        self.addAxiomButton.clicked.connect(self.get_new_axiom)
        self.removeAxiomButton.clicked.connect(self.remove_axiom)

        self.axiomList = QListWidget(self)
        self.axiomList.addItems([])

        self.generateButton = QPushButton(self)
        self.generateButton.setText("Generate")
        self.generateButton.clicked.connect(self.generate)

        self.label = QLabel(self)

        self.label.setText("")

        self.createGridLayout()
        self.show()

        self.data = Data()

    def createGridLayout(self):
        layout = QGridLayout()

        layout.addWidget(self.label, 0, 0, 8, 1)
        layout.addWidget(self.rulesListTitle, 0, 1, 1, 1)
        layout.addWidget(self.rulesList, 1, 1, 1, 2)
        layout.addWidget(self.addRuleButton, 2, 1, 1, 1)
        layout.addWidget(self.removeRuleButton, 2, 2, 1, 1)
        layout.addWidget(self.iterationsTitle, 3, 1, 1, 2)
        layout.addWidget(self.iterations, 4, 1, 1, 2)
        layout.addWidget(self.angleTitle, 5, 1, 1, 2)
        layout.addWidget(self.angle, 6, 1, 1, 2)
        layout.addWidget(self.axiomListTitle, 7, 1, 1, 2)
        layout.addWidget(self.axiomList, 8, 1, 1, 2)
        layout.addWidget(self.addAxiomButton, 9, 1, 1, 1)
        layout.addWidget(self.removeAxiomButton, 9, 2, 1, 1)
        layout.addWidget(self.generateButton, 10, 1, 1, 2)
        # layout.addWidget(self.addLSysButton, 0, 1)
        # layout.addWidget(self.generateButton, 1, 1)
        # layout.addWidget(self.show_button, 2, 1)

        layout.setColumnStretch(0, 5)

        self.setLayout(layout)

    def get_new_rule(self):
        rule_entry = RuleInputDialog(self)
        result = rule_entry.exec()
        if result:
            key = rule_entry.keyEntry.text()
            value = rule_entry.valueEntry.text()
            self.data.add_rule(key, value)

            rule_str = key + " -> " + value
            self.rulesList.addItem(rule_str)

    def get_new_axiom(self):
        axiom_entry = AxiomInputDialog(self)
        result = axiom_entry.exec()
        if result:
            axiom = axiom_entry.axiomEntry.text()
            self.data.add_axiom(axiom)
            self.axiomList.addItem(axiom)

    def remove_rule(self):
        current_item = self.rulesList.currentItem()
        self.rulesList.takeItem(int(self.rulesList.row(current_item)))

    def remove_axiom(self):
        current_item = self.axiomList.currentItem()
        self.axiomList.takeItem(int(self.axiomList.row(current_item)))

    def update_label(self):
        items = self.data.rules.items()
        s = "\n".join(str(r) + " -> " + str(k) for r, k in items)
        self.label.setText("Rules:\n" + s)

    def rule_str_to_dict(self, rule_str):
        rule_dict = dict([rule_str.split(" -> ")])
        return rule_dict

    def generate(self):
        try:
            rules = self.data.rules
            assert self.data.rules is not {}
            axiom = self.axiomList.currentItem().text()
            angle = self.angle.value()
            lsys = Lsys(self.data.alphabet, rules)
            if int(self.iterations.value()) != 0:
                g = Generator(lsys, axiom, angle, self.iterations.value())
                steps, history, stack = g.generate_tortoise()
                from lsystems.draw import draw_coords

                im = draw_coords(history, 200).copy()
                # self.data.img = im
                fmt = QImage.Format.Format_Grayscale8
                qimage = QImage(im, im.shape[0], im.shape[1], fmt)
                pixmap = QPixmap(qimage)
                self.label.setPixmap(pixmap)

        except AttributeError:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                """Please input rule(s) and axiom(s), 
                and make sure an axiom is selected."""
            )
            error_dialog.exec()

    def showOnLabel(self):
        pixmap = QPixmap("image.jpg")
        self.label.setPixmap(pixmap)


class Data:
    def __init__(self):
        self.rules = {}
        self.axioms = []

        self.alphabet = ["F", "f", "+", "-"]

    def add_rule(self, key, value):
        self.rules[key] = value

    def add_axiom(self, axiom):
        self.axioms.append(axiom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
