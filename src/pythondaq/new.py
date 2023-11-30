import sys
from pythondaq.diode_experiment import DiodeExperiment

from PySide6 import QtWidgets


class UserInterface(QtWidgets.QMainWindow):
    def __init__():
        super.__init__()
        model = DiodeExperiment()
        data = model.scan(0, 1023, 100)
        return data


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()  