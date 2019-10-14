import PySide2
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets


class ConnectablePort(QtWidgets.QGraphicsItem):

    def __init__(self, parent=None):
        super(ConnectablePort, self).__init__(parent)

        self.setAcceptHoverEvents(True)
        self.setFlags(self.ItemIsSelectable)

        self.setZValue(2)
        self._portSize = 10.0
        self.port_type = None
        self.adjacentList = []
        self._hovered = False

    def boundingRect(self):
        return QtCore.QRectF(0.0, 0.0, self._portSize, self._portSize)

    def paint(self, painter, option, widget):
        painter.save()

        rect = QtCore.QRectF(0.0, 0.8, self._portSize, self._portSize)
        painter.setBrush(PySide2.QtGui.QColor(0, 0, 0, 200))
        painter.setPen(PySide2.QtGui.QPen(PySide2.QtGui.QColor(0, 0, 0, 255), 1.8))
        path = PySide2.QtGui.QPainterPath()
        path.addEllipse(rect)
        painter.drawPath(path)

        if self._hovered:
            _portColor = PySide2.QtGui.QColor(100, 96, 100, 255)
            _portBorderColor = PySide2.QtGui.QColor(136, 255, 35, 255)
        else:
            _portColor = PySide2.QtGui.QColor(29, 80, 84, 255)
            _portBorderColor = PySide2.QtGui.QColor(45, 215, 255, 255)

        painter.setBrush(_portColor)
        pen = PySide2.QtGui.QPen(_portBorderColor, 2)
        painter.setPen(pen)
        painter.drawEllipse(self.boundingRect())

        painter.restore()

    def hoverEnterEvent(self, event):
        self._hovered = True
        super(ConnectablePort, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hovered = False
        super(ConnectablePort, self).hoverLeaveEvent(event)

    def isLeftEdge(self, node):
        for edge in self.adjacentList:
            if node == edge.leftNode:
                return False
        return True

    def isInputEdge(self, node):
        for edge in self.adjacentList:
            if node == edge.rightNode:
                return False
        return True
