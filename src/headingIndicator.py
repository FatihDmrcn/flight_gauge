import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import numpy as np


class NavigationDisplay(qtw.QWidget):

    pink = qtg.QColor(255, 92, 205, 255)
    white = qtc.Qt.white

    def __init__(self, size, *args, **kwargs):
        super(NavigationDisplay, self).__init__(*args, **kwargs)
        if size < 300:
            size = 300
        self.setFixedSize(int((4/3)*size), size)
        self.unit = self.height()/100
        self.pivot = self.height()*0.9
        self.scale_wp = 1.2
        self.r = self.pivot-self.unit*9

        self.hdg = np.linspace(1, 36, num=36)
        self.hdg_half = np.linspace(0.5, 35.5, num=36)
        self.w = self.unit*6

        self.wps = [{"WP": "EDDK", "COORD": (self.unit*5, -self.unit*5)},
                    {"WP": "EDDV", "COORD": (self.unit*10, -self.unit*23.5)},
                    {"WP": "EDDB", "COORD": (self.unit*15, -self.unit*40)}]

        # Font
        self.font = qtg.QFont("Courier New")
        self.font.setWeight(61)
        self.font.setPixelSize(int(4*self.unit))
        self.setFont(self.font)
        # Background
        self.setAutoFillBackground(True)
        palette = qtg.QPalette()
        palette.setColor(self.backgroundRole(), qtc.Qt.black)
        self.setPalette(palette)
        # Initial Heading
        self.heading = 0
        
    def setAngle(self, heading):
        self.heading = heading
        self.repaint()
        
    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.translate(self.width() / 2, self.pivot)
        painter.setRenderHints(qtg.QPainter.HighQualityAntialiasing, True)

        # Pen
        pen = qtg.QPen()
        pen.setWidthF(self.unit/2)
        pen.setColor(self.white)
        pen.setJoinStyle(qtc.Qt.MiterJoin)
        painter.setPen(pen)
        # Brush
        brush = qtg.QBrush()
        brush.setStyle(qtc.Qt.SolidPattern)
        brush.setColor(qtc.Qt.transparent)

        self.paint_heading_indicator(painter)
        self.paint_aircraft_indicator(painter)
        self.paint_waypoints(painter, pen)

    def paint_heading_indicator(self, painter):
        painter.save()
        # Heading Clipper
        painter.setClipPath(self.clipper_polygon_heading())
        # Heading Circle
        painter.drawEllipse(self.heading_circle())
        # Heading Strokes and Angles
        painter.save()
        painter.rotate(-self.heading)
        for h in self.hdg:
            painter.save()
            painter.rotate(h * 10)
            painter.drawLine(0, self.r, 0, self.r - 4 * self.unit)
            if h % 3 == 0:
                painter.drawText(qtc.QRectF(-self.w / 2, -self.r + self.w / 2, self.w, self.w), qtc.Qt.AlignCenter, str(int(h)))
            painter.restore()
        for h in self.hdg_half:
            painter.save()
            painter.rotate(h * 10)
            painter.drawLine(0, self.r, 0, self.r - 1.5 * self.unit)
            painter.restore()
        painter.restore()
        painter.restore()

    def clipper_polygon_heading(self):
        cathetus = 1.1 * self.r * np.sin(45 * np.pi/180)
        clip_path_polygon = (qtc.QPointF(0, 0), qtc.QPointF(-cathetus, -cathetus), qtc.QPointF(-cathetus, -self.pivot),
                             qtc.QPointF(cathetus, -self.pivot), qtc.QPointF(cathetus, -cathetus))
        clip_path_heading = qtg.QPainterPath()
        clip_path_heading.addPolygon(qtg.QPolygonF(clip_path_polygon))
        return clip_path_heading

    def heading_circle(self):
        return qtc.QRectF(-self.r, -self.r, 2*self.r, 2*self.r)

    def paint_aircraft_indicator(self, painter):
        painter.save()
        painter.drawPolygon(self.aircraft_indicator_static())
        painter.restore()

    def aircraft_indicator_static(self):
        triangle_static = (qtc.QPointF(-self.unit * 2.75, self.unit * 5), qtc.QPointF(self.unit * 2.75, self.unit * 5),
                           qtc.QPointF(0, 0))
        return qtg.QPolygonF(triangle_static)

    def paint_waypoints(self, painter, pen):
        painter.save()
        # Waypoint Clipper
        painter.setClipPath(self.clipper_polygon_waypoint())
        # Waypoint Setting
        painter.scale(self.scale_wp, self.scale_wp)
        painter.rotate(-self.heading)
        pen.setWidthF(self.unit / (2 * self.scale_wp))
        painter.setPen(pen)
        # Waypoint Draw Line
        pen.setColor(self.pink)
        painter.setPen(pen)
        painter.drawPath(self.waypoint_path())
        # Waypoint Draw Waypoints
        pen.setColor(self.white)
        painter.setPen(pen)
        for wp in self.wps:
            painter.save()
            x = wp["COORD"][0]
            y = wp["COORD"][1]
            painter.translate(x, y)
            painter.rotate(self.heading)
            # Draw Stars
            painter.drawPolygon(self.waypoint_star_polygon())
            # Draw Names
            painter.save()
            painter.scale(1 / self.scale_wp, 1 / self.scale_wp)
            painter.drawText(qtc.QRectF(self.unit * 2.5, -self.unit * 2.5, self.unit * 20, -self.unit * 5), 0x0081, wp["WP"])
            painter.restore()
            painter.restore()
        painter.restore()

    def waypoint_star_polygon(self):
        _l = self.unit * 2.5 / self.scale_wp
        _c = self.unit * 0.75 / self.scale_wp
        waypoint_star = (qtc.QPointF(-_l, 0), qtc.QPointF(-_c, -_c), qtc.QPointF(0, -_l), qtc.QPointF(_c, -_c),
                         qtc.QPointF(_l, 0), qtc.QPointF(_c, _c), qtc.QPointF(0, _l), qtc.QPointF(-_c, _c))
        return qtg.QPolygonF(waypoint_star)

    def clipper_polygon_waypoint(self):
        clip_path_rectangular = qtc.QRectF(-0.9 * self.r, -0.9 * self.r, 1.8 * self.r, 1.8 * self.r)
        clip_path_wp = qtg.QPainterPath()
        clip_path_wp.addRoundedRect(clip_path_rectangular, self.r, self.r)
        return clip_path_wp

    def waypoint_path(self):
        wp_path = qtg.QPainterPath(qtc.QPointF(0, 0))
        for wp in self.wps:
            x = float(wp["COORD"][0])
            y = float(wp["COORD"][1])
            wp_path.lineTo(qtc.QPointF(x, y))
        return wp_path
