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
    def __init__(self, size, *args, **kwargs):
        super(PrimaryFlightDisplay, self).__init__(*args, **kwargs)
        if size<300:size=300
        self.setFixedSize((4/3)*size,size)
        self.unit = self.height()/100
        #Scaling
        self.rollScale = 0.9
        self.aircraftScale = 0.6
        self.pitchPadding = 1.5
        #Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(5*self.unit)
        self.setFont(self.font)
        #Values
        self.pitchAngle = 0                          #Initial Pitch
        self.rollAngle = 0                           #Initial Roll
        
    def setAngle(self, pitch, roll):
        self.pitchAngle = pitch*self.unit*self.pitchPadding
        self.rollAngle = roll
        self.repaint()
        
    def paintEvent(self,event):
        painterPFD = qtg.QPainter(self)
        painterPFD.translate(self.width()/2,self.height()/2)
        
        
        #Colors
        blue = qtg.QColor(0, 64, 128, 255)
        brown = qtg.QColor(120, 64, 0, 255)
        #Pen
        pen = qtg.QPen()
        pen.setWidthF(self.unit/2)
        pen.setColor(qtc.Qt.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painterPFD.setPen(pen)
        #Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)
        painterPFD.setBrush(brush)
        
        
        #Horizon Indicator Begin
        painterPFD.save()
        pen.setColor(qtc.Qt.transparent)
        painterPFD.setPen(pen)
        painterPFD.rotate(-self.rollAngle)
        painterPFD.translate(0,self.pitchAngle)
        x = -self.unit*300
        w = self.unit*600
        h = self.unit*3000
        sky = qtc.QRectF(x,-self.unit*3000,w,h)
        ground = qtc.QRectF(x,0,w,h)
        brush.setColor(blue)
        painterPFD.setBrush(brush)
        painterPFD.drawRect(sky)
        brush.setColor(brown)
        painterPFD.setBrush(brush)
        painterPFD.drawRect(ground)
        painterPFD.restore()
        #Horizon Indicator End
        
        
        #Pitch Indicator Begin
        painterPFD.save()
        pen.setColor(qtc.Qt.white)
        painterPFD.setPen(pen)
        painterPFD.setRenderHints(qtg.QPainter.HighQualityAntialiasing,
                                       qtg.QPainter.TextAntialiasing)
        painterPFD.rotate(-self.rollAngle)
        painterPFD.translate(0,self.pitchAngle)
        #Pitch Horizon Line
        painterPFD.drawLine(-self.unit*300,0,self.unit*300,0)
        #Pitch Clipper
        r = self.unit*43*self.rollScale             #Radius
        clipPathCircle = qtc.QRectF(-r,-self.pitchAngle-r,2*r,2*r)
        clipPath = qtg.QPainterPath()
        clipPath.addEllipse(clipPathCircle)
        painterPFD.setClipPath(clipPath)
        #Pitch Circle
        circle = qtc.QRectF(-self.unit*2,-self.unit*2,self.unit*4,self.unit*4)
        painterPFD.drawEllipse(circle)
        #Pitch Angle Lines
        pitchMain = np.linspace(10,90,num=9)
        pitchHalf = np.linspace(5,85,num=9)
        pitchQuarter = np.linspace(2.5,92.5,num=19)
        for p in pitchMain:
            x = self.unit*13                        #x-Position
            y = p*self.unit*self.pitchPadding       #y-Position
            painterPFD.drawLine(-x,y,x,y)           #Upper Lines
            painterPFD.drawLine(-x,-y,x,-y)         #Lower Lines
            w = self.unit*10                        #Width
            h = self.unit*6                         #Height
            s = str(int(p))                         #Pitch Angle
            a = qtc.Qt.AlignCenter                  #Alignment
            painterPFD.drawText(qtc.QRectF(-x-w,y-h/2,w,h),a,s)
            painterPFD.drawText(qtc.QRectF(-x-w,-y-h/2,w,h),a,s)
            painterPFD.drawText(qtc.QRectF(x,y-h/2,w,h),a,s)
            painterPFD.drawText(qtc.QRectF(x,-y-h/2,w,h),a,s)
        for p in pitchHalf:
            x = self.unit*6.5
            y = p*self.unit*self.pitchPadding
            painterPFD.drawLine(-x,y,x,y)           #Upper Lines
            painterPFD.drawLine(-x,-y,x,-y)         #Lower Lines
        for p in pitchQuarter:
            x = self.unit*2.5
            y = p*self.unit*self.pitchPadding
            painterPFD.drawLine(-x,y,x,y)           #Upper Lines
            painterPFD.drawLine(-x,-y,x,-y)         #Lower Lines
        painterPFD.restore()
        #Pitch Indicator End
        
        
        #Roll Indicator Begin
        painterPFD.save()
        painterPFD.scale(self.rollScale,self.rollScale)
        pen.setWidthF((self.unit/2)/self.rollScale)
        painterPFD.setPen(pen)
        painterPFD.setRenderHints(qtg.QPainter.HighQualityAntialiasing)       
        #Roll Indicator Dynamic Triangle
        painterPFD.save()
        painterPFD.rotate(-self.rollAngle)
        triangleDynamic = (qtc.QPointF(-self.unit*2.25,-self.unit*40),
                           qtc.QPointF(self.unit*2.25,-self.unit*40),
                           qtc.QPointF(self.unit*0,-self.unit*44))
        triangleDynamicPoly = qtg.QPolygonF(triangleDynamic)
        painterPFD.drawPolygon(triangleDynamicPoly)
        painterPFD.restore()
        #Roll Indicator Static Triangle
        brush.setColor(qtc.Qt.white)
        painterPFD.setBrush(brush)
        triangleStatic = (qtc.QPointF(-self.unit*1.75,-self.unit*47.5),
                          qtc.QPointF(self.unit*1.75,-self.unit*47.5),
                          qtc.QPointF(self.unit*0,-self.unit*44.5))
        triangleStaticPoly = qtg.QPolygonF(triangleStatic)
        painterPFD.drawPolygon(triangleStaticPoly)
        #Roll Indicator Static Strokes
        smallStrokes = (-45,-20,-10,10,20,45)
        for s in smallStrokes:
            painterPFD.save()
            painterPFD.rotate(s)
            painterPFD.drawLine(0,-self.unit*47.5,0,-self.unit*44.5)
            painterPFD.restore()
        bigStrokes = (-60,-30,30,60)
        for b in bigStrokes:
            painterPFD.save()
            painterPFD.rotate(b)
            painterPFD.drawLine(0,-self.unit*50.5,0,-self.unit*44.5)
            painterPFD.restore()
        painterPFD.restore()
        #Roll Indicator End
        
        
        #Aircraft Indicator Begin
        painterPFD.save()
        painterPFD.scale(self.aircraftScale,self.aircraftScale)
        pen.setWidthF(self.unit*3)
        painterPFD.setPen(pen)
        #Aircraft Indicator Left Wing
        lWingPath = qtg.QPainterPath(qtc.QPointF(-self.unit*45,0))
        lWingPath.lineTo(qtc.QPointF(-self.unit*15,0))
        lWingPath.lineTo(qtc.QPointF(-self.unit*15,self.unit*5))
        #Aircraft Indicator Right Wing
        rWingPath = qtg.QPainterPath(qtc.QPointF(self.unit*45,0))
        rWingPath.lineTo(qtc.QPointF(self.unit*15,0))
        rWingPath.lineTo(qtc.QPointF(self.unit*15,self.unit*5))
        #Aircraft Indicator Center Box
        painterPFD.drawPath(lWingPath)
        painterPFD.drawPath(rWingPath)
        painterPFD.drawPoint(qtc.QPointF(0,0))
        painterPFD.restore()
        #Aircraft Indicator End