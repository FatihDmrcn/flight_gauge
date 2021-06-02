# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:50:35 2020
@author: FDemircan
"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import numpy as np

class Gauge(qtw.QWidget):
    def __init__(self, size, maxValue, minValue=0, *args, **kwargs):
        super(Gauge, self).__init__(*args, **kwargs)
        if size<75:size=75
        self.setFixedSize(1.5*size,size)
        self.unit = self.height()/100
        self.maxAngle = 210                        #Max Angle of Indication
        #Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(17.5*self.unit)
        self.setFont(self.font)
        #Background
        self.setAutoFillBackground(True)
        palette = qtg.QPalette()
        palette.setColor(self.backgroundRole(), qtc.Qt.black)
        self.setPalette(palette)
        #Values
        self.value = 0
        self.maxValue = maxValue
        self.minValue = minValue
        self.angle = self.valueToAngle(self.value)
        
    def setValue(self,value):
        self.value = value
        self.angle = self.valueToAngle(self.value)
        self.repaint()
        
    def valueToAngle(self,value):
        return self.maxAngle*(self.value-self.minValue)/(self.maxValue-self.minValue)
        
    def paintEvent(self,event):
        painterGauge = qtg.QPainter(self)
        painterGauge.translate(self.width()/2,self.height()/2)
        painterGauge.setRenderHints(qtg.QPainter.HighQualityAntialiasing,
                                    qtg.QPainter.TextAntialiasing)
        
        
        #Pen
        pen = qtg.QPen()
        pen.setWidthF(2*self.unit)
        pen.setColor(qtc.Qt.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painterGauge.setPen(pen)
        #Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)
                
        
        #Radial Indicator Begin
        painterGauge.save()
        painterGauge.scale(0.7,0.7)
        h = self.height()
        r = (h/2)*0.9
        #Radial Indicator Arc
        pen.setWidthF(self.unit*4)
        pen.setCapStyle(qtc.Qt.FlatCap)
        painterGauge.setPen(pen)
        arcRect = qtc.QRectF(-h/2,-h/2,h,h)
        painterGauge.drawArc(arcRect,0,-self.maxAngle*16)
        #Radial Indicator Pie
        brush.setColor(qtc.Qt.gray)
        painterGauge.setBrush(brush)
        pen.setColor(qtc.Qt.transparent)
        painterGauge.setPen(pen)
        pieRect = qtc.QRectF(-r,-r,2*r,2*r)
        painterGauge.drawPie(pieRect,0,-self.angle*16)      #Degree in 1/16
        #Radial Max Stroke
        pen.setColor(qtc.Qt.red)
        pen.setCapStyle(qtc.Qt.SquareCap)
        painterGauge.setPen(pen)
        opp = np.sin((self.maxAngle-180)*np.pi/180)         #Opposed Cathetus
        adj = np.cos((self.maxAngle-180)*np.pi/180)         #Adjacent Cathetus
        painterGauge.drawLine(-adj*h/2,-opp*h/2,
                              -adj*(1.2*h/2),
                              -opp*(1.2*h/2))
        #Radial Indicator Bar
        painterGauge.save()
        painterGauge.rotate(self.angle)
        pen.setColor(qtc.Qt.white)
        pen.setCapStyle(qtc.Qt.RoundCap)
        painterGauge.setPen(pen)
        painterGauge.drawLine(0,0,r-self.unit,0)
        painterGauge.restore()
        painterGauge.restore()
        #Radial Indicator End
        
        
        #Box Indicator Begin
        painterGauge.save()
        yBox = -0.275*h
        hBox = 0.225*h
        boxRect = qtc.QRectF(0,yBox,0.65*h,hBox)
        painterGauge.drawRect(boxRect)
        textRect = qtc.QRectF(0.05,yBox,0.6*h,hBox)
        painterGauge.drawText(textRect,0x0082,str(round(100*self.angle/self.maxAngle,1)))
        painterGauge.restore()
        #Box Indicator End