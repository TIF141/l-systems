from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
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
