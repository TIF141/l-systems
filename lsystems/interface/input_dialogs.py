from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QButtonGroup,
    QPushButton,
    QGridLayout,
)

from lsystems.utils import rule_dict_to_str, rule_str_to_dict


class RuleInputDialog(QDialog):
    def __init__(self, parent=None, editing=False):
        super().__init__(parent)

        # self.parent = parent
        if parent is not None:
            self.data = parent.data
        self.createItems(editing)
        self.generateLayout()

    def createItems(self, editing):
        self.keyEntry = QLineEdit()
        self.valueEntry = QLineEdit()

        if editing:
            current_rule = self.parent().rulesList.currentItem().text()
            rule_dict = rule_str_to_dict(current_rule)
            key, value = list(rule_dict.keys())[0], list(rule_dict.values())[0]
            self.keyEntry.setText(key)
            self.valueEntry.setText(value)
        else:
            self.keyEntry.setPlaceholderText("Enter rule key")

            self.valueEntry.setPlaceholderText("Enter rule value")

        # self.iterationsEntry = QSpinBox()
        # self.iterationsEntry.setMinimum(0)

        self.buttons = QDialogButtonBox(self)
        cancel = QDialogButtonBox.StandardButton.Cancel
        ok = QDialogButtonBox.StandardButton.Ok
        self.buttons.setStandardButtons(cancel | ok)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # self.okButton = QPushButton()
        # self.okButton.setText("Create rule")
        # self.okButton.clicked.connect(self.add_rule)

    def generateLayout(self):
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.keyEntry)
        self.lay.addWidget(self.valueEntry)
        # self.layout.addWidget(self.iterationsEntry)
        self.lay.addWidget(self.buttons)
        self.setLayout(self.lay)

    def accept(self):
        validInput = self.checkInput()
        if validInput:
            self.done(1)

    def checkInput(self):
        if self.keyEntry.text() == "":
            return False
        if self.valueEntry.text() == "":
            return False
        return True


class AxiomInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.data = parent.data
        self.createItems()
        self.generateLayout()

    def createItems(self):
        self.axiomEntry = QLineEdit()
        self.axiomEntry.setPlaceholderText("Enter axiom")

        self.buttons = QDialogButtonBox(self)
        cancel = QDialogButtonBox.StandardButton.Cancel
        ok = QDialogButtonBox.StandardButton.Ok
        self.buttons.setStandardButtons(cancel | ok)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # self.okButton = QPushButton()
        # self.okButton.setText("Create rule")
        # self.okButton.clicked.connect(self.add_rule)

    def generateLayout(self):
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.axiomEntry)
        # self.layout.addWidget(self.iterationsEntry)
        self.lay.addWidget(self.buttons)
        self.setLayout(self.lay)

    def accept(self):
        validInput = self.checkInput()
        if validInput:
            self.done(1)

    def checkInput(self):
        if self.axiomEntry.text() == "":
            return False
        return True


class AddRuleSetDialog(QDialog):
    def __init__(self, parent=None, editing=False):
        super().__init__(parent)

        if parent is not None:
            self.data = parent.data

        self.editing = editing

        self.createItems(editing)
        self.generateLayout()

        if editing:
            current_ruleset = self.parent().rulesetList.currentItem().text()
            self.rulesDict = self.parent().data.rules[current_ruleset]
        else:
            self.rulesDict = {}

    def createItems(self, editing):
        # Rule set name
        self.ruleSetName = QLabel()
        self.ruleNameBox = QLineEdit()
        self.rulesList = QListWidget()
        self.addRemoveButtons = QButtonGroup(self)
        self.addRuleButton = QPushButton()
        self.editRuleButton = QPushButton()
        self.removeRuleButton = QPushButton()

        if editing:
            current_ruleset = self.parent().rulesetList.currentItem().text()
            current_rules = self.parent().data.rules[current_ruleset]
            rules_str = rule_dict_to_str(current_rules)
            self.ruleNameBox.setText(current_ruleset)
            self.rulesList.addItems(rules_str)

        self.ruleSetName.setText("Ruleset name")
        self.ruleNameBox.setPlaceholderText("Enter ruleset name")
        self.addRemoveButtons.addButton(self.addRuleButton)
        self.addRemoveButtons.addButton(self.addRuleButton)
        self.addRemoveButtons.addButton(self.removeRuleButton)
        self.addRuleButton.setText("Add rule")
        self.editRuleButton.setText("Edit rule")
        self.removeRuleButton.setText("Remove rule")
        self.addRuleButton.clicked.connect(self.add_rule)
        self.editRuleButton.clicked.connect(self.edit_rule)
        self.removeRuleButton.clicked.connect(self.remove_rule)
        self.okCancelButtons = QDialogButtonBox(self)
        cancel = QDialogButtonBox.StandardButton.Cancel
        ok = QDialogButtonBox.StandardButton.Ok
        self.okCancelButtons.setStandardButtons(cancel | ok)
        self.okCancelButtons.accepted.connect(self.accept)
        self.okCancelButtons.rejected.connect(self.reject)
        pass

    def generateLayout(self):
        layout = QGridLayout()

        layout.addWidget(self.ruleSetName, 0, 0, 1, 3)
        layout.addWidget(self.ruleNameBox, 1, 0, 1, 3)
        layout.addWidget(self.rulesList, 2, 0, 1, 3)
        layout.addWidget(self.addRuleButton, 3, 0, 1, 1)
        layout.addWidget(self.editRuleButton, 3, 1, 1, 1)
        layout.addWidget(self.removeRuleButton, 3, 2, 1, 1)
        layout.addWidget(self.okCancelButtons, 4, 0, 1, 3)

        self.setLayout(layout)

    def accept(self):
        validInput = self.checkInput()
        if validInput:
            self.done(1)

    def checkInput(self):
        if self.ruleNameBox.text() == "":
            return False
        if self.ruleNameBox.text() in self.data.rules.keys():
            if not self.editing:
                return False
        if self.rulesList.count() == 0:
            return False
        return True

    def add_rule(self):
        rule_entry = RuleInputDialog(self)
        result = rule_entry.exec()
        if result:
            key = rule_entry.keyEntry.text()
            value = rule_entry.valueEntry.text()
            rule_str = key + " -> " + value
            self.rulesList.addItem(rule_str)
            self.rulesDict[key] = value

    def edit_rule(self):
        if len(self.rulesList.selectedItems()) == 0:
            return
        rule_entry = RuleInputDialog(self, editing=True)
        result = rule_entry.exec()
        if result:
            key = rule_entry.keyEntry.text()
            value = rule_entry.valueEntry.text()
            rule_str = key + " -> " + value
            current_rule_str = self.rulesList.currentItem().text()
            if rule_str != current_rule_str:
                self.rulesList.currentItem().setText(rule_str)
                current_dict = rule_str_to_dict(current_rule_str)
                current_key, current_value = list(current_dict.items())[0]
                del self.rulesDict[current_key]
                self.rulesDict[key] = value

    def remove_rule(self):
        if len(self.rulesList.selectedItems()) == 0:
            return
        current_item = self.rulesList.currentItem()
        self.rulesList.takeItem(int(self.rulesList.row(current_item)))
