import sys
from pythondaq.diode_experiment import DiodeExperiment
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6 import QtWidgets
import numpy as np
import pyqtgraph as pg
import csv

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

        label_start = QtWidgets.QLabel("Set minimum")
        hbox.addWidget(label_start)

        start_button = QtWidgets.QSpinBox(minimum= 0, maximum=1023, value =0)
        hbox.addWidget(start_button)
        start_button.valueChanged.connect(self.start)

        label_stop = QtWidgets.QLabel("Set maximum")
        hbox.addWidget(label_stop)

        stop_button = QtWidgets.QSpinBox(minimum=0, maximum=1023, value = 1023)
        hbox.addWidget(stop_button)
        stop_button.valueChanged.connect(self.stop)

        label_repeat = QtWidgets.QLabel("Set repeats")
        hbox.addWidget(label_repeat)

        repeat_button = QtWidgets.QSpinBox(minimum = 1, value = 1)
        hbox.addWidget(repeat_button)
        repeat_button.valueChanged.connect(self.repeat)

        save_button = QtWidgets.QPushButton("save")
        hbox.addWidget(save_button)
        save_button.clicked.connect(self.save_data)

        self.min = 0
        self.max = 1023
        self.N = 1

        self.std_I = []
        self.gem_I = []
        self.std_U = []
        self.gem_U = []
    @Slot()
    def scan(self, min, max, N):
        model = DiodeExperiment(port="ASRL9::INSTR")
        data = model.scan(min, max, N)
        
        print(data)
        print(min, max, N)
 

        return data
    
    @Slot()
    def plot(self):
        self.plot_widget.clear()
        data = self.scan(self.min, self.max, self.N)
        self.std_I = data[3]
        self.gem_I = data[2]
        self.std_U = data[1]
        self.gem_U = data[0]
        self.plot_widget.plot(self.gem_U, self.gem_I, symbol="o", symbolSize=5, pen=None)
        error_bars = pg.ErrorBarItem(x=np.array(self.gem_U), y=np.array(self.gem_I), width=2 * np.array(self.std_U), height=2 * np.array(self.std_I))
        self.plot_widget.addItem(error_bars)
        # self.plot_widget.setLabel("left", "sin(x)")
        # self.plot_widget.setLabel("bottom", "x [radians]")

    @Slot()
    def clear(self):
        self.plot_widget.clear()

    @Slot()
    def start(self, min):
        self.min = min

    @Slot()
    def stop(self, max):
        self.max=max

    @Slot()
    def repeat(self, N):
        self.N = N

    @Slot()
    def save_data(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        with open(f'{filename}', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['U', 'std_U', 'I', 'std_I'])
                for a, b, c, d in zip(self.gem_U, self.std_U, self.gem_I, self.std_I):
                    writer.writerow([a, b, c, d])
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()