import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import attitudeIndicator as ai
import headingIndicator as hi
import gaugeIndicator as gi
import sys

class mk1(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mk1")
        self.grid = qtw.QGridLayout()
        self.grid.setSpacing(0)
        self.pfd = ai.PrimaryFlightDisplay(300)
        self.nd = hi.NavigationDisplay(300)
        
        self.gauge = [[gi.Gauge(75,90,-90) for j in range(2)] for i in range(4)]
        
        self.slider = qtw.QSlider(qtc.Qt.Horizontal)
        self.slider.setMinimum(-900)
        self.slider.setMaximum(900)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.values)
        
        self.grid.addWidget(self.pfd,0,0,4,1)
        self.grid.addWidget(self.nd,0,1,4,1)
        for i in range(4):
            for j in range(2):
                self.grid.addWidget(self.gauge[i][j],i,2+j)
        self.grid.addWidget(self.slider,4,0,1,4)
        self.setLayout(self.grid)
        self.show()
        
    def values(self):
        v = self.slider.value()/10
        self.pfd.setAngle(v,v)
        self.nd.setAngle(v)
        for i in range(4):
            for j in range(2):
                self.gauge[i][j].setValue(v)
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ui = mk1()
    sys.exit(app.exec_())
