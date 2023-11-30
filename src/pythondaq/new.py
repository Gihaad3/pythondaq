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
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.plot_widget = pg.PlotWidget()

        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_widget)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        plot_button =  QtWidgets.QPushButton("Plot")
        hbox.addWidget(plot_button)
        plot_button.clicked.connect(self.plot)

    @  Slot()
    def scan(self, min, max, N):
        model = DiodeExperiment(port="ASRL9::INSTR")
        data = model.scan(min, max, N)

        return data
    
    @Slot()
    def plot(self):
        data = self.scan(0, 1023, 1)
        self.plot_widget.clear()
        self.plot_widget.plot(data[3], data[1], symbol="o", pen={"color": "w", "width": 5})
        self.plot_widget.setLabel("left", "sin(x)")
        self.plot_widget.setLabel("bottom", "x [radians]")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()