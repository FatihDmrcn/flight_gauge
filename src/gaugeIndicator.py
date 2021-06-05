import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import numpy as np

class Gauge(qtw.QWidget):
    def __init__(self, size, max_value, min_value=0, *args, **kwargs):
        super(Gauge, self).__init__(*args, **kwargs)
        if size < 75:
            size = 75
        self.setFixedSize(int(1.5*size),size)
        self.unit = self.height()/100
        self.maxAngle = 210                        #Max Angle of Indication
        self.r = (self.height()/2)*0.9
        # Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(int(17.5*self.unit))
        self.setFont(self.font)
        # Background
        self.setAutoFillBackground(True)
        palette = qtg.QPalette()
        palette.setColor(self.backgroundRole(), qtc.Qt.black)
        self.setPalette(palette)
        # Values
        self.value = 0
        self.maxValue = max_value
        self.minValue = min_value
        self.angle = self.valueToAngle(self.value)
        
    def setValue(self,value):
        self.value = value
        self.angle = self.valueToAngle(self.value)
        self.repaint()
        
    def valueToAngle(self,value):
        return self.maxAngle*(self.value-self.minValue)/(self.maxValue-self.minValue)
        
    def paintEvent(self,event):
        painter = qtg.QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setRenderHints(qtg.QPainter.HighQualityAntialiasing, True)

        # Pen
        pen = qtg.QPen()
        pen.setWidthF(2*self.unit)
        pen.setColor(qtc.Qt.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painter.setPen(pen)
        # Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)

        self.paint_radial_indicator_static(painter, pen, brush)
        self.paint_radial_indicator_bar(painter, pen)
        self.paint_box_indicator(painter)

    def paint_radial_indicator_static(self, painter, pen, brush):
        painter.save()
        painter.scale(0.9, 0.9)

        # Radial Indicator Arc
        pen.setWidthF(self.unit*4)
        pen.setCapStyle(qtc.Qt.FlatCap)
        painter.setPen(pen)
        arc_rect = qtc.QRectF(-self.height() / 2, -self.height() / 2, self.height(), self.height())
        painter.drawArc(arc_rect, 0, -self.maxAngle * 16)

        # Radial Indicator Pie
        brush.setColor(qtc.Qt.gray)
        painter.setBrush(brush)
        pen.setColor(qtc.Qt.transparent)
        painter.setPen(pen)
        pie_rect = qtc.QRectF(-self.r, -self.r, 2 * self.r, 2 * self.r)
        painter.drawPie(pie_rect, 0, -self.angle * 16)      #Degree in 1/16

        # Radial Max Stroke
        pen.setColor(qtc.Qt.red)
        pen.setCapStyle(qtc.Qt.SquareCap)
        painter.setPen(pen)
        # Opposed Cathetus
        opp = np.sin((self.maxAngle-180) * np.pi/180)
        # Adjacent Cathetus
        adj = np.cos((self.maxAngle-180) * np.pi/180)
        painter.drawLine(-adj * self.height() / 2, -opp * self.height() / 2,
                         -adj * (1.2*self.height()/2), -opp * (1.2*self.height()/2))
        painter.restore()

    def paint_radial_indicator_bar(self, painter, pen):
        painter.save()
        painter.rotate(self.angle)
        pen.setColor(qtc.Qt.white)
        pen.setCapStyle(qtc.Qt.SquareCap)
        painter.setPen(pen)
        painter.drawLine(0, 0, self.r - self.unit, 0)
        painter.restore()

    def paint_box_indicator(self, painter):
        painter.save()
        y_box = -0.275 * self.height()
        h_box = 0.225 * self.height()
        box_rect = qtc.QRectF(0, y_box, 0.65 * self.height(), h_box)
        painter.drawRect(box_rect)
        text_rect = qtc.QRectF(0.05, y_box, 0.6 * self.height(), h_box)
        painter.drawText(text_rect, 0x0082, str(round(100 * self.angle / self.maxAngle, 1)))
        painter.restore()
