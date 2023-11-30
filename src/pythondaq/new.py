import sys
from pythondaq.diode_experiment import DiodeExperiment
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6 import QtWidgets
import numpy as np
import pyqtgraph as pg

class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_widget = pg.PlotWidget()

    @  Slot()
    def scan(self):
        model = DiodeExperiment(port="ASRL9::INSTR")
        data = model.scan(0, 1023, 100, )

        return data
    @Slot()
    def plot(self):
        self.plot_widget.clear()
        x = np.linspace(-np.pi, np.pi, 100)
        self.plot_widget.plot(x, np.sin(x), symbol=None, pen={"color": "k", "width": 5})
        self.plot_widget.setLabel("left", "sin(x)")
        self.plot_widget.setLabel("bottom", "x [radians]")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()