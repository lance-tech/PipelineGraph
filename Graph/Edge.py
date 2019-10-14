import PySide2
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
from Graph import NodeUtil


class Arrow(QtWidgets.QGraphicsPathItem):
    def __init__(self, parent=None, scene=None):
        super(Arrow, self).__init__(parent, scene)
        self.setVisible(False)
        self.setZValue(0)
        self.color = PySide2.QtGui.QColor(127, 149, 151, 255)
        self.pos1 = QtCore.QPoint(0.0, 0.0)
        self.pos2 = QtCore.QPoint(0.0, 0.0)
        
    def boundingRect(self):
        return QtCore.QRectF(-10.0, -10.0, 20.0, 20.0)

    def paint(self, painter, option, widget):
        pen = PySide2.QtGui.QPen(self.color, 2)
        painter.setPen(pen)
        
        v1 = PySide2.QtGui.QVector2D(self.pos1)
        v2 = PySide2.QtGui.QVector2D(self.pos2)
        direction = v2.__sub__(v1)
        direction.normalize()
        direction = direction.__mul__(8)

        _centerVec = PySide2.QtGui.QVector2D(QtCore.QPoint(0, 0))
        _arrowHeadVec = _centerVec.__add__(direction)

        verticalUpVec = PySide2.QtGui.QVector2D(QtCore.QPoint(direction.y(), -direction.x()))
        verticalUpVec = verticalUpVec.__mul__(0.4)
        verticalUpVec = _centerVec.__add__(verticalUpVec)
        verticalDownVec = _centerVec.__add__(-verticalUpVec)

        painter.drawLine(_centerVec.toPoint(), verticalUpVec.toPoint())
        painter.drawLine(_centerVec.toPoint(), verticalDownVec.toPoint())

        painter.drawLine(verticalUpVec.toPoint(), _arrowHeadVec.toPoint())
        painter.drawLine(verticalDownVec.toPoint(), _arrowHeadVec.toPoint())
        painter.drawLine(_centerVec.toPoint(), _arrowHeadVec.toPoint())


class Edge(QtWidgets.QGraphicsPathItem):
    def __init__(self, leftPort=None, rightPort=None):
        super(Edge, self).__init__()
        self.setFlags(self.ItemIsSelectable)

        self.setZValue(-1)

        self.leftPort = leftPort
        self.rightPort = rightPort

        self.leftPort.adjacentList.append(self)
        if self.rightPort:
            self.rightPort.adjacentList.append(self)

        self.startPos = QtCore.QPoint(0, 0)
        self.endPos = QtCore.QPoint(0, 0)

        self.ctlPos1 = QtCore.QPoint(0, 0)
        self.ctlPos2 = QtCore.QPoint(0, 0)

        self.arrowSpeed = 150
        self.interval = None
        self._arrows = []

        self._time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimeLoop)

        self.isAnimation = False
        self.defaultArrow = None

        self.initializeArrow()

        self.updateDraw()

    def initializeArrow(self):
        self.defaultArrow = Arrow(self)
        self.defaultArrow.setVisible(True)

        arrowCount = 5
        for _ in range(arrowCount):
            _arrow = Arrow(self)
            _arrow.color = QtCore.Qt.yellow
            self._arrows.append(_arrow)
        self.interval = 1.0 / arrowCount

    def startArrowAnimation(self):
        self.timer.start(30)
        self.isAnimation = True
        for arrow in self._arrows:
            arrow.setVisible(True)

    def stopArrowAnimation(self):
        self.timer.stop()
        self.isAnimation = False
        for arrow in self._arrows:
            arrow.setVisible(False)

    def updateTimeLoop(self):
        self.update()

        self._time += 1
        if self._time > self.arrowSpeed:
            self._time = 0

    def setRightPort(self, port):
        self.rightPort = port
        self.rightPort.adjacentList.append(self)

    def paint(self, painter, option, widget):
        color = PySide2.QtGui.QColor(127, 149, 151, 255)
        self.defaultArrow.color = color
        pen_width = 3
        if self.isSelected():
            color = PySide2.QtGui.QColor(232, 184, 13, 255)
            self.defaultArrow.color = color
            pen_width = 5

        pen_style = QtCore.Qt.PenStyle.SolidLine

        pen = PySide2.QtGui.QPen(color, pen_width)
        pen.setStyle(pen_style)
        pen.setCapStyle(QtCore.Qt.RoundCap)

        painter.setPen(pen)
        painter.setRenderHint(painter.Antialiasing, True)
        painter.drawPath(self.path())

        if self.isAnimation:
            self.drawArrow()

    def getPointOnCurve(self, t):
        t = t % 1.0

        _p1 = self.ctlPos1.__sub__(self.startPos).__mul__(t).__add__(self.startPos)
        _p2 = self.ctlPos2.__sub__(self.ctlPos1).__mul__(t).__add__(self.ctlPos1)
        _p3 = self.endPos.__sub__(self.ctlPos2).__mul__(t).__add__(self.ctlPos2)

        _tp1 = _p2.__sub__(_p1).__mul__(t).__add__(_p1)
        _tp2 = _p3.__sub__(_p2).__mul__(t).__add__(_p2)

        return _tp2.__sub__(_tp1).__mul__(t).__add__(_tp1)

    def drawArrow(self):
        if self.startPos:
            for i in range(len(self._arrows)):
                offset = self.interval * i
                t1 = (self._time / float(self.arrowSpeed)) + offset

                pos1 = self.getPointOnCurve(t1)
                self._arrows[i].pos1 = pos1

                self._arrows[i].setPos(pos1)

                t1_post = t1 + 0.001

                pos2 = self.getPointOnCurve(t1_post)
                self._arrows[i].pos2 = pos2


    def updateDraw(self, pos=None):
        self.draw_path(self.leftPort, self.rightPort, pos)

        t1 = 0.55
        pos1 = self.getPointOnCurve(t1)
        self.defaultArrow.pos1 = pos1
        self.defaultArrow.setPos(pos1)
        t1_post = t1 + 0.001

        pos2 = self.getPointOnCurve(t1_post)
        self.defaultArrow.pos2 = pos2

    def draw_path(self, leftPort, rightPort, cursor_pos=None):
        if not leftPort:
            return
        offset = (leftPort.boundingRect().width() / 2)
        pos1 = leftPort.scenePos()
        pos1.setX(pos1.x() + offset)
        pos1.setY(pos1.y() + offset)

        if cursor_pos:
            pos2 = cursor_pos
        elif rightPort:
            offset = leftPort.boundingRect().width() / 2
            pos2 = rightPort.scenePos()
            pos2.setX(pos2.x() + offset)
            pos2.setY(pos2.y() + offset)
        else:
            return

        self.startPos = pos1
        self.endPos = pos2

        path = PySide2.QtGui.QPainterPath()
        path.moveTo(pos1)

        ctr_offset_x1, ctr_offset_x2 = pos1.x(), pos2.x()
        tangent = ctr_offset_x1 - ctr_offset_x2
        tangent = (tangent * -1) if tangent < 0 else tangent

        max_width = leftPort.parentItem().boundingRect().width() / 2
        tangent = max_width if tangent > max_width else tangent

        if leftPort.port_type == NodeUtil.LEFT_PORT:
            ctr_offset_x1 -= tangent
            ctr_offset_x2 += tangent
        elif leftPort.port_type == NodeUtil.RIGHT_PORT:
            ctr_offset_x1 += tangent
            ctr_offset_x2 -= tangent

        self.ctlPos1 = QtCore.QPointF(ctr_offset_x1, pos1.y())
        self.ctlPos2 = QtCore.QPointF(ctr_offset_x2, pos2.y())

        path.cubicTo(self.ctlPos1, self.ctlPos2, pos2)

        self.setPath(path)

    def removeEdge(self):
        self.leftPort.adjacentList.remove(self)
        self.scene().removeItem(self)

    def disconnect(self):
        self.leftPort.adjacentList.remove(self)
        self.rightPort.adjacentList.remove(self)
        self.scene().removeItem(self)
    
    @property
    def leftNode(self):
        return self.leftPort.parentItem()

    @property
    def rightNode(self):
        return self.rightPort.parentItem()