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


class RuleInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
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


class AddRuleSetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.data = parent.data

        self.createItems()
        self.generateLayout()

        self.rulesDict = {}

    def createItems(self):
        # Rule set name
        self.ruleSetName = QLabel()
        self.ruleSetName.setText("Ruleset name")
        # Text
        self.ruleNameBox = QLineEdit()
        self.ruleNameBox.setPlaceholderText("Enter ruleset name")
        # Rules: list
        self.rulesList = QListWidget()
        # Buttons: add, edit, remove
        self.addRemoveButtons = QButtonGroup(self)
        self.addRuleButton = QPushButton()
        self.editRuleButton = QPushButton()
        self.removeRuleButton = QPushButton()
        self.addRemoveButtons.addButton(self.addRuleButton)
        self.addRemoveButtons.addButton(self.editRuleButton)
        self.addRemoveButtons.addButton(self.removeRuleButton)
        self.addRuleButton.setText("Add rule")
        self.editRuleButton.setText("Edit rule")
        self.removeRuleButton.setText("Remove rule")
        self.addRuleButton.clicked.connect(self.add_rule)
        # self.editRuleButton.clicked.connect(self.edit_rule)
        self.removeRuleButton.clicked.connect(self.remove_rule)
        # self.addRuleButton.clicked.connect(self.add_rule)
        # self.editRuleButton.clicked.connect(self.edit_rule)
        # self.removeRuleButton.clicked.connect(self.remove_rule)
        # Buttons: ok, cancel
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

    def add_rule(self):
        rule_entry = RuleInputDialog(self)
        result = rule_entry.exec()
        if result:
            key = rule_entry.keyEntry.text()
            value = rule_entry.valueEntry.text()
            rule_str = key + " -> " + value
            self.rulesList.addItem(rule_str)
            self.rulesDict[key] = value

    def remove_rule(self):
        current_item = self.rulesList.currentItem()
        self.rulesList.takeItem(int(self.rulesList.row(current_item)))
