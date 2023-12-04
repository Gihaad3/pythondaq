import sys
from pythondaq.diode_experiment import DiodeExperiment, list_devices, close
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import numpy as np
import pyqtgraph as pg
import csv

class UserInterface(QtWidgets.QMainWindow):
    """This class creates an graphical user interface(GUI) that can plot and/or save the data from a experiment, the variables of the experiment can be changed, those are the minimum and maximum(3.3 Volts) voltage in volts and the number of times the experiment is repeated.
    """

    def __init__(self):
        """This method creates the lay-out of the GUI with vertical and horizontal layouts, and creates the buttons.
        """

        # Calls the __init__() of the parent class
        super().__init__()

        # This creates a central- and plot widget and adds it to the vertical layout 
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_widget)

        # This creates an horizontal layout and adds it to the vertical layout
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        # This is the label for the minimum value button
        label_start = QtWidgets.QLabel("Set minimum")
        hbox.addWidget(label_start)

        # This creates a button that can change the minimum voltage in volts trough the start method
        start_button = QtWidgets.QDoubleSpinBox(minimum=0, maximum=3.3, value=0, singleStep=0.1)
        hbox.addWidget(start_button)
        start_button.valueChanged.connect(self.start)

        # This creates a label for the maximum value button
        label_stop = QtWidgets.QLabel("Set maximum")
        hbox.addWidget(label_stop)

        # This creates a button that can change the maximum voltage in volts trough the stop method
        stop_button = QtWidgets.QDoubleSpinBox(minimum=0, maximum=3.3, value=3.3, singleStep=0.1)
        hbox.addWidget(stop_button)
        stop_button.valueChanged.connect(self.stop)

        # This creates a label for the number of repeats value button
        label_repeat = QtWidgets.QLabel("Set repeats")
        hbox.addWidget(label_repeat)

        # This creates a  button that can change the number of repeats through the repeat method
        repeat_button = QtWidgets.QSpinBox(minimum=1, value=1)
        hbox.addWidget(repeat_button)
        repeat_button.valueChanged.connect(self.repeat)

        # Here all the devices are given in a list
        self.lists = list_devices()

        # This is the label for the device selection menu
        label_choose = QtWidgets.QLabel("Choose device")
        hbox.addWidget(label_choose)

        # Here a selection menu is created with the list of devices
        choose_device = QtWidgets.QComboBox()
        choose_device.addItems(self.lists)
        hbox.addWidget(choose_device)
        choose_device.currentIndexChanged.connect(self.port)

        # This creates another horizontal layout and adds it to the vertical layout
        hbox_2 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_2)

        # This creates and adds a button to the GUI, when pressed the method plot is activated
        plot_button =  QtWidgets.QPushButton("Plot")
        hbox_2.addWidget(plot_button)
        plot_button.clicked.connect(self.plot)

        # This creates and adds a button to the GUI, when pressed the method save is activated
        save_button = QtWidgets.QPushButton("save")
        hbox_2.addWidget(save_button)
        save_button.clicked.connect(self.save_data)

        # This creates and adds a button to the GUI, when pressed the method clear is activated
        clear_button = QtWidgets.QPushButton("Clear")
        hbox_2.addWidget(clear_button)
        clear_button.clicked.connect(self.clear)

        # THis creates and adds a button to the GUI, when pressed the method close is activated
        quit_button = QtWidgets.QPushButton("Quit")
        hbox_2.addWidget(quit_button)
        quit_button.clicked.connect(self.close)

        # Minimum and maximum voltage in ADC units
        self.min = 0
        self.max = 1023
      
        # Number of repeats and port
        self.N = 1
        self.ports = 0

        # These are all the used lists
        self.std_I = []
        self.gem_I = []
        self.std_U = []
        self.gem_U = []
        
        # I set the default device 
        self.port(self.ports)

        # I name the axis of the plot
        self.plot_widget.setLabel("left", "Average current trough LED in amperes")
        self.plot_widget.setLabel("bottom", "Average voltage over LED in volts")
   

    @Slot()
    def scan(self, min, max, N):
        """This method sends an interval of voltage in units ADC through the circuit and collects the data.

        Args:
            min (int): the minimum voltage
            max (int): the maximum voltage
            N (int): the number of repeats

        Returns:
            tuple: This tuple has respectively the data for the average voltage, the standard defiation of the voltage, the average current and the standard deviation of the current.
        """        
        model = DiodeExperiment(port=self.ports)
        data = model.scan(min, max, N)
        close()

        return data
    

    @Slot()
    def plot(self):
        """This method clears the current plot and plots the new data with errorbars.
        """

        # The previous plot is cleared
        self.plot_widget.clear()

        #  the collected data
        data = self.scan(self.min, self.max, self.N)
    
        self.std_I = data[3]
        self.gem_I = data[2]
        self.std_U = data[1]
        self.gem_U = data[0]

        # This plots the data and adds the errorbars in a graph   
        self.plot_widget.plot(self.gem_U, self.gem_I, symbol="o", symbolSize=5, pen=None)
        error_bars = pg.ErrorBarItem(x=np.array(self.gem_U), y=np.array(self.gem_I), width=2 * np.array(self.std_U), height=2 * np.array(self.std_I))
        self.plot_widget.addItem(error_bars)


    @Slot()
    def clear(self):
        """This method clears the plot widget
        """
        self.plot_widget.clear()


    @Slot()
    def close(self):
        """This method closes the GUI
        """  
        quit()


    @Slot()
    def start(self, min):
        """This method converts volts to ADC and changes the minimum value.

        Args:
            min (int): This is minimum voltage in volts send over the circuit
        """
        min_ADC = int(1023/3.3 * min)
        self.min = min_ADC


    @Slot()
    def stop(self, max):
        """This method converts volts to ADC and changes the maximum value.

        Args:
            max (int): This is the maximum voltage in volts over the circuit
        """  
        max_ADC = int(1023/3.3 * max)
        self.max= max_ADC


    @Slot()
    def repeat(self, N):
        """This method changes the number of times the experiment is repeated.

        Args:
            N (int): The number of times the experiment is repeated
        """   
        self.N = N


    @Slot()
    def save_data(self):
        """This creates a csv file with a given name and stores the data in it.
        """
        # This allowes the file to be created and the name be given
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        
        # The data is stored in a csv file
        with open(f'{filename}', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['U', 'std_U', 'I', 'std_I'])
            for a, b, c, d in zip(self.gem_U, self.std_U, self.gem_I, self.std_I):
                writer.writerow([a, b, c, d])


    @Slot()
    def port(self, ports):
        """This changes the device which conducts the experiment

        Args:
            ports (string): The name of the chosen device
        """        
        self.ports = self.lists[ports]


def main():
    """This function opens the GUI
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())



# This runs the function that opens the GUI
if __name__ == "__main__":
    main()