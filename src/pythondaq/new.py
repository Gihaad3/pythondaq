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

        clear_button = QtWidgets.QPushButton("Clear")
        vbox.addWidget(clear_button)
        clear_button.clicked.connect(self.clear)

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
        # self.plot_widget.clear()
        data = self.scan(0, 1023, 1)
        std_I = data[0]
        gem_I = data[1]
        std_U = data[2]
        gem_U = data[3]
        self.plot_widget.plot(gem_U, gem_I, symbol="o", symbolSize=5, pen=None)
        # error_bars = pg.ErrorBarItem(x=gem_U, y=gem_I, width=2 * np.array(std_U), height=2 * np.array(std_I))
        # self.plot_widget.addItem(error_bars)
        # self.plot_widget.setLabel("left", "sin(x)")
        # self.plot_widget.setLabel("bottom", "x [radians]")

    @Slot()
    def clear(self):
        self.plot_widget.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()