if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from lsystems.interface.gui import Window

    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
