# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:34:18 2020
@author: FDemircan
"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import numpy as np

class NavigationDisplay(qtw.QWidget):
    def __init__(self, size, *args, **kwargs):
        super(NavigationDisplay, self).__init__(*args, **kwargs)
        if size<300:size=300
        self.setFixedSize((4/3)*size,size)
        self.unit = self.height()/100
        self.pivot = self.height()*0.9
        self.scaleWP = 1.2
        #Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(4*self.unit)
        self.setFont(self.font)
        #Background
        self.setAutoFillBackground(True)
        palette = qtg.QPalette()
        palette.setColor(self.backgroundRole(), qtc.Qt.black)
        self.setPalette(palette)
        #Values
        self.heading = 0                                #Initial Heading
        
    def setAngle(self,heading):
        self.heading = heading
        self.repaint()
        
    def paintEvent(self,event):
        painterND = qtg.QPainter(self)
        painterND.translate(self.width()/2,self.pivot)
        painterND.setRenderHints(qtg.QPainter.HighQualityAntialiasing,
                                 qtg.QPainter.TextAntialiasing)
        
        
        #Colors
        pink = qtg.QColor(255, 92, 205, 255)
        #Pen
        pen = qtg.QPen()
        pen.setWidthF(self.unit/2)
        pen.setColor(qtc.Qt.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painterND.setPen(pen)
        #Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)
        
        
        #Heading Indicator Begin
        painterND.save()
        r = self.pivot-self.unit*9                      #Main Radius
        #Heading Clipper
        cathetus = 1.1*r*np.sin(45*np.pi/180)
        clipPathPoly = (qtc.QPointF(0,0),
                        qtc.QPointF(-cathetus,-cathetus),
                        qtc.QPointF(-cathetus,-self.pivot),
                        qtc.QPointF(cathetus,-self.pivot),
                        qtc.QPointF(cathetus,-cathetus))
        clipPathHDG = qtg.QPainterPath()
        clipPathHDG.addPolygon(qtg.QPolygonF(clipPathPoly))
        painterND.setClipPath(clipPathHDG)
        #Heading Circle
        #headingCircle = qtc.QRectF(-r,-r,2*r,2*r)
        #painterND.drawEllipse(headingCircle)
        #Heading Strokes and Angles
        hdg = np.linspace(1,36,num=36)
        hdg_half = np.linspace(0.5,35.5,num=36)
        w = self.unit*6
        painterND.save()
        painterND.rotate(-self.heading)
        for h in hdg:
            painterND.save()
            painterND.rotate(h*10)
            painterND.drawLine(0,r,0,r-4*self.unit)
            if h%3==0:
                h = str(int(h))                         #Heading
                a = qtc.Qt.AlignCenter                  #Alignment
                painterND.drawText(qtc.QRectF(-w/2,-r+w/2,w,w),a,h)
            painterND.restore()
        for h in hdg_half:
            painterND.save()
            painterND.rotate(h*10)
            painterND.drawLine(0,r,0,r-1.5*self.unit)
            painterND.restore()
        painterND.restore()
        painterND.restore()
        #Heading Indicator End


        #Aircraft Indicator Begin
        painterND.save()
        triangleStatic = (qtc.QPointF(-self.unit*2.75,self.unit*5),
                          qtc.QPointF(self.unit*2.75,self.unit*5),
                          qtc.QPointF(0,0))
        triangleStaticPoly = qtg.QPolygonF(triangleStatic)
        painterND.drawPolygon(triangleStaticPoly)
        painterND.restore()
        #Aircraft Indicator End
        
        
        #Waypoint Indicator Begin
        painterND.save()
        #Waypoint Clipper
        clipPathRectF = qtc.QRectF(-0.9*r,-0.9*r,1.8*r,1.8*r)
        clipPathWP = qtg.QPainterPath()
        clipPathWP.addRoundedRect(clipPathRectF,r,r)
        painterND.setClipPath(clipPathWP)
        #Waypoint Setting
        painterND.scale(self.scaleWP,self.scaleWP)
        painterND.rotate(-self.heading)
        pen.setWidthF(self.unit/(2*self.scaleWP))
        painterND.setPen(pen)
        #Waypoint Define
        wps = [{"WP":"TCKK","COORD":(self.unit*5,-self.unit*5)},
            {"WP":"KKTC","COORD":(self.unit*10,-self.unit*23.5)},
            {"WP":"KTCK","COORD":(self.unit*15,-self.unit*40)}]
        #Waypoint Draw Line
        wpPath = qtg.QPainterPath(qtc.QPointF(0,0))
        for wp in wps:
            x = wp["COORD"][0]
            y = wp["COORD"][1]
            wpPath.lineTo(qtc.QPointF(x,y))
        pen.setColor(pink)
        painterND.setPen(pen)
        painterND.drawPath(wpPath)
        #Waypoint Draw Waypoints
        pen.setColor(qtc.Qt.white)
        painterND.setPen(pen)
        l = self.unit*2.5/self.scaleWP
        c = self.unit*0.75/self.scaleWP
        u = self.unit*2.5
        for wp in wps:
            painterND.save()
            x = wp["COORD"][0]
            y = wp["COORD"][1]
            painterND.translate(x,y)
            painterND.rotate(self.heading)
            #Draw Stars
            wpStar = (qtc.QPointF(-l,0),qtc.QPointF(-c,-c),
                      qtc.QPointF(0,-l),qtc.QPointF( c,-c),
                      qtc.QPointF( l,0),qtc.QPointF( c, c),
                      qtc.QPointF(0, l),qtc.QPointF(-c, c))
            wpStarPoly = qtg.QPolygonF(wpStar)
            painterND.drawPolygon(wpStarPoly)
            #Draw Names
            painterND.save()
            painterND.scale(1/self.scaleWP,1/self.scaleWP)
            painterND.drawText(qtc.QRectF(u,-u,8*u,-2*u),0x0081,wp["WP"])
            painterND.restore()
            painterND.restore()
        painterND.restore()
        #Waypoint Indicator End