import sys

from PySide6 import QtWidgets


class UserInterface(QtWidgets.QMainWindow):
    pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()  