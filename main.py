import PyQt5.QtWidgets as Qtw
import PyQt5.QtCore as Qtc
from src.attitudeIndicator import PrimaryFlightDisplay
from src.headingIndicator import NavigationDisplay
from src.gaugeIndicator import Gauge
import sys


class Mk1(Qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mk1")
        self.grid = Qtw.QGridLayout()
        self.grid.setSpacing(0)
        self.pfd = PrimaryFlightDisplay(300)
        self.nd = NavigationDisplay(300)
        
        self.gauge = [[Gauge(75, 90, -90) for j in range(2)] for i in range(4)]
        
        self.slider = Qtw.QSlider(Qtc.Qt.Horizontal)
        self.slider.setMinimum(-900)
        self.slider.setMaximum(900)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.values)
        
        self.grid.addWidget(self.pfd, 0, 0, 4, 1)
        self.grid.addWidget(self.nd, 0, 1, 4, 1)
        for i in range(4):
            for j in range(2):
                self.grid.addWidget(self.gauge[i][j], i, 2+j)
        self.grid.addWidget(self.slider, 4, 0, 1, 4)
        self.setLayout(self.grid)
        self.show()
        
    def values(self):
        v = self.slider.value()/10
        self.pfd.set_angle(v, v)
        self.nd.set_angle(v)
        for i in range(4):
            for j in range(2):
                self.gauge[i][j].set_value(v)


if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    ui = Mk1()
    sys.exit(app.exec_())
