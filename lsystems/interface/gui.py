import sys
import re
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QRegularExpressionValidator as QRegExValidator

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
from lsystems.interface.input_dialogs import (
    RuleInputDialog,
    AxiomInputDialog,
    AddRuleSetDialog,
)

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
        self.editRuleButton = QPushButton()
        self.removeRuleButton = QPushButton()
        self.addRuleButton.setText("Add ruleset")
        self.editRuleButton.setText("Edit ruleset")
        self.removeRuleButton.setText("Remove ruleset")
        self.rulesButtons.addButton(self.addRuleButton)
        self.rulesButtons.addButton(self.editRuleButton)
        self.rulesButtons.addButton(self.removeRuleButton)
        self.addRuleButton.clicked.connect(self.get_new_rule)
        self.editRuleButton.clicked.connect(self.edit_rule)
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
        layout.addWidget(self.rulesList, 1, 1, 1, 3)
        layout.addWidget(self.addRuleButton, 2, 1, 1, 1)
        layout.addWidget(self.editRuleButton, 2, 2, 1, 1)
        layout.addWidget(self.removeRuleButton, 2, 3, 1, 1)
        layout.addWidget(self.iterationsTitle, 3, 1, 1, 3)
        layout.addWidget(self.iterations, 4, 1, 1, 3)
        layout.addWidget(self.angleTitle, 5, 1, 1, 3)
        layout.addWidget(self.angle, 6, 1, 1, 3)
        layout.addWidget(self.axiomListTitle, 7, 1, 1, 3)
        layout.addWidget(self.axiomList, 8, 1, 1, 3)
        layout.addWidget(self.addAxiomButton, 9, 1, 1, 1)
        layout.addWidget(self.removeAxiomButton, 9, 2, 1, 1)
        layout.addWidget(self.generateButton, 10, 1, 1, 3)
        # layout.addWidget(self.addLSysButton, 0, 1)
        # layout.addWidget(self.generateButton, 1, 1)
        # layout.addWidget(self.show_button, 2, 1)

        layout.setColumnStretch(0, 5)

        self.setLayout(layout)

    def get_new_rule(self):
        # rule_entry = RuleInputDialog(self)
        ruleset_entry = AddRuleSetDialog(self, editing=False)
        result = ruleset_entry.exec()
        if result:
            rulesetName = ruleset_entry.ruleNameBox.text()
            rulesDict = ruleset_entry.rulesDict
            self.data.add_ruleset(rulesetName, rulesDict)

            # rule_str = key + " -> " + value
            self.rulesList.addItem(rulesetName)

    def edit_rule(self):
        ruleset_entry = AddRuleSetDialog(self, editing=True)
        result = ruleset_entry.exec()
        if result:
            rulesetName = ruleset_entry.ruleNameBox.text()
            rulesDict = ruleset_entry.rulesDict
            old_name = self.rulesList.currentItem().text()
            del self.data.rules[old_name]
            self.data.add_ruleset(rulesetName, rulesDict)
            self.rulesList.currentItem().setText(rulesetName)

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
            current_ruleset = self.rulesList.currentItem().text()
            rules = self.data.rules[current_ruleset]
            assert rules
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

    # def add_rule(self, key, value):
    #     valid_entry = self.assert_valid_entry(key, value)
    #     if not valid_entry:
    #         error_dialog = QErrorMessage()
    #         error_dialog.showMessage("""Please input valid key and value.""")
    #         return error_dialog.exec()

    #     else:
    #         self.rules[key] = value
    #         return

    def add_ruleset(self, name, rules):
        for k, v in rules.items():
            # valid_entry = self.assert_valid_entry(k, v)
            valid_entry = True
            if not valid_entry:
                error_dialog = QErrorMessage()
                error_dialog.showMessage("""Please input valid rules""")
                return error_dialog.exec()

            else:
                self.rules[name] = rules

    def add_axiom(self, axiom):
        self.axioms.append(axiom)

    def assert_valid_entry(self, key, value):
        key_error = any(c not in self.alphabet for c in str(key))
        value_error = any(c not in self.alphabet for c in str(value))
        return not key_error and not value_error


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
