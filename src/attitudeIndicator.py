# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 20:14:27 2020
@author: FDemircan
"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import numpy as np


class PrimaryFlightDisplay(qtw.QWidget):

    blue = qtg.QColor(0, 64, 128, 255)
    brown = qtg.QColor(120, 64, 0, 255)
    white = qtc.Qt.white

    def __init__(self, size, *args, **kwargs):
        super(PrimaryFlightDisplay, self).__init__(*args, **kwargs)
        if size<300:size=300
        self.setFixedSize(int((4/3)*size), size)
        self.unit = self.height()/100
        # Scaling
        self.rollScale = 0.9
        self.aircraftScale = 0.6
        self.pitchPadding = 1.5
        # Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(int(5*self.unit))
        self.setFont(self.font)
        # Values
        # Initial Pitch
        self.pitchAngle = 0
        # Initial Roll
        self.rollAngle = 0
        
    def setAngle(self, pitch, roll):
        self.pitchAngle = pitch*self.unit*self.pitchPadding
        self.rollAngle = roll
        self.repaint()
        
    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setRenderHints(qtg.QPainter.HighQualityAntialiasing, True)

        # Pen
        pen = qtg.QPen()
        pen.setWidthF(self.unit/2)
        pen.setColor(qtc.Qt.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painter.setPen(pen)
        # Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)
        painter.setBrush(brush)

        self.paint_horizon_indicator(painter, pen, brush)
        self.paint_pitch_indicator(painter, pen)
        self.paint_roll_indicator(painter, pen, brush)
        self.paint_aircraft_indicator(painter, pen)

    def paint_horizon_indicator(self, painter, pen, brush):
        painter.save()
        pen.setColor(qtc.Qt.transparent)
        painter.setPen(pen)
        painter.rotate(-self.rollAngle)
        painter.translate(0, self.pitchAngle)
        x = -self.unit*300
        w = self.unit*600
        h = self.unit*3000

        sky = qtc.QRectF(x, -h, w, h)
        brush.setColor(self.blue)
        painter.setBrush(brush)
        painter.drawRect(sky)

        ground = qtc.QRectF(x, 0, w, h)
        brush.setColor(self.brown)
        painter.setBrush(brush)
        painter.drawRect(ground)
        painter.restore()

    def paint_pitch_indicator(self, painter, pen):
        painter.save()
        pen.setColor(self.white)
        painter.setPen(pen)
        painter.rotate(-self.rollAngle)
        painter.translate(0, self.pitchAngle)
        # Pitch Horizon Line
        painter.drawLine(-self.unit * 300, 0, self.unit * 300, 0)
        # Pitch Clipper
        r = self.unit*43*self.rollScale             #Radius
        clipPathCircle = qtc.QRectF(-r,-self.pitchAngle-r,2*r,2*r)
        clipPath = qtg.QPainterPath()
        clipPath.addEllipse(clipPathCircle)
        painter.setClipPath(clipPath)
        # Pitch Circle
        circle = qtc.QRectF(-self.unit*2,-self.unit*2,self.unit*4,self.unit*4)
        painter.drawEllipse(circle)
        # Pitch Angle Lines
        pitchMain = np.linspace(10,90,num=9)
        pitchHalf = np.linspace(5,85,num=9)
        pitchQuarter = np.linspace(2.5,92.5,num=19)
        for p in pitchMain:
            x = self.unit*13                        #x-Position
            y = p*self.unit*self.pitchPadding       #y-Position
            painter.drawLine(-x, y, x, y)           #Upper Lines
            painter.drawLine(-x, -y, x, -y)         #Lower Lines
            w = self.unit*10                        #Width
            h = self.unit*6                         #Height
            s = str(int(p))                         #Pitch Angle
            a = qtc.Qt.AlignCenter                  #Alignment
            painter.drawText(qtc.QRectF(-x - w, y - h / 2, w, h), a, s)
            painter.drawText(qtc.QRectF(-x - w, -y - h / 2, w, h), a, s)
            painter.drawText(qtc.QRectF(x, y - h / 2, w, h), a, s)
            painter.drawText(qtc.QRectF(x, -y - h / 2, w, h), a, s)
        for p in pitchHalf:
            x = self.unit*6.5
            y = p*self.unit*self.pitchPadding
            painter.drawLine(-x, y, x, y)           #Upper Lines
            painter.drawLine(-x, -y, x, -y)         #Lower Lines
        for p in pitchQuarter:
            x = self.unit*2.5
            y = p*self.unit*self.pitchPadding
            painter.drawLine(-x, y, x, y)           #Upper Lines
            painter.drawLine(-x, -y, x, -y)         #Lower Lines
        painter.restore()

    def paint_roll_indicator(self, painter, pen, brush):
        painter.save()
        painter.scale(self.rollScale, self.rollScale)
        pen.setWidthF((self.unit/2)/self.rollScale)
        painter.setPen(pen)

        # Roll Indicator Dynamic Triangle
        painter.save()
        painter.rotate(-self.rollAngle)
        painter.drawPolygon(self.roll_indicator_triangle('dyn'))
        painter.restore()

        # Roll Indicator Static Triangle
        brush.setColor(self.white)
        painter.setBrush(brush)
        painter.drawPolygon(self.roll_indicator_triangle('sta'))

        # Roll Indicator Static Strokes
        small_strokes = (-45, -20, -10, 10, 20, 45)
        for s in small_strokes:
            painter.save()
            painter.rotate(s)
            painter.drawLine(0, -self.unit * 47.5, 0, -self.unit * 44.5)
            painter.restore()
        big_strokes = (-60, -30, 30, 60)
        for b in big_strokes:
            painter.save()
            painter.rotate(b)
            painter.drawLine(0, -self.unit * 50.5, 0, -self.unit * 44.5)
            painter.restore()
        painter.restore()

    def roll_indicator_triangle(self, state):
        n = {'dyn': {'w': 2.25, 'c': 44, 'a': 40},
             'sta': {'w': 1.75, 'c': 44.5, 'a': 47.5}}
        triangle = (qtc.QPointF(-self.unit * 2.25, -self.unit * n[state]['a']),
                    qtc.QPointF(self.unit* 2.25, -self.unit * n[state]['a']),
                    qtc.QPointF(0, -self.unit * n[state]['c']))
        triangle_polygon = qtg.QPolygonF(triangle)
        return triangle_polygon

    def paint_aircraft_indicator(self, painter, pen):
        painter.save()
        painter.scale(self.aircraftScale, self.aircraftScale)
        pen.setWidthF(self.unit*3)
        painter.setPen(pen)
        # Wings
        painter.drawPath(self.wing_path('l'))
        painter.drawPath(self.wing_path('r'))
        # Center Box
        painter.drawPoint(qtc.QPointF(0, 0))
        painter.restore()

    def wing_path(self, side):
        vz = {'l': -1, 'r': +1}
        wing_path = qtg.QPainterPath(qtc.QPointF(vz[side]*self.unit * 45, 0))
        wing_path.lineTo(qtc.QPointF(vz[side]*self.unit * 15, 0))
        wing_path.lineTo(qtc.QPointF(vz[side]*self.unit * 15, self.unit * 5))
        return wing_path
