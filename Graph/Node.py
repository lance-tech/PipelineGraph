import os
import PySide2
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets

from Graph.ConnectablePort import ConnectablePort
from Graph.ProxyWidget import ProxyWidgetLabel
from Graph.ProxyWidget import ProxyWidgetToolButton
from Graph.ProxyWidget import ProxyWidgetTable
import Graph.NodeUtil as NodeUtil

class Node(QtWidgets.QGraphicsItem):
    def __init__(self, _type, _id=None, parent=None):
        super(Node, self).__init__(parent)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setZValue(2)
        self._id = _id

        self.type = _type
        self.color = NodeUtil.NODE_COLOR.user
        
        self.version = 1
        self._width = 180
        self.isExtended = False

        self.leftPort = ConnectablePort(self)
        self.leftPort.port_type = NodeUtil.LEFT_PORT
        portX = self.leftPort._portSize
        self.leftPort.setPos(-portX, 10.0)

        self.rightPort = ConnectablePort(self)
        self.rightPort.port_type = NodeUtil.RIGHT_PORT
        self.rightPort.setPos(self._width, 10.0)

        _nodeData = NodeUtil.getNodeInitialData(self.type)
        self.name = _nodeData['name']
        self.widget_taskLabel = ProxyWidgetLabel(self, self.name)
        self.widget_taskLabel.setPos(10, 8)
        self.color = _nodeData['color'].value

        self.widget_pubButton = ProxyWidgetToolButton(self, 'Pub')
        offset = self.widget_pubButton.size().width() + 8
        self.widget_pubButton.setPos(self._width - offset, 4)
        self.widget_pubButton.widget.clicked.connect(self._pubButtonHandle)

        self.pubFileTable = ProxyWidgetTable(self, 'Publish Files')
        self.pubFileTable.setPos(8, 37)

        self.originHeight = 53 + self.pubFileTable.size().height()
        self._height = self.originHeight

        self.foldNode()

    def boundingRect(self):
        return QtCore.QRectF(0.0, 0.0, self._width, self._height)

    def paint(self, painter, option, widget):
        painter.save()

        radius = 5
        # Node Body
        rect = self.boundingRect()
        bg_color = PySide2.QtGui.QColor(*self.color)

        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundRect(rect, radius, radius)

        # Node Title Label
        label_rect = QtCore.QRectF(rect.left() + (radius / 2),
                                   rect.top() + (radius / 2),
                                   self._width - (radius / 1.25),
                                   28)
        path = PySide2.QtGui.QPainterPath()
        path.addRoundedRect(label_rect, radius / 1.5, radius / 1.5)
        painter.setBrush(PySide2.QtGui.QColor(0, 0, 0, 30))
        painter.fillPath(path, painter.brush())

        # Node Selection Highlight
        border_width = 0.8
        border_color = PySide2.QtGui.QColor(85, 100, 100, 255)
        if self.isSelected():
            border_width = 3.0
            border_color = PySide2.QtGui.QColor(254, 207, 42, 255)
        border_rect = QtCore.QRectF(rect.left() - (border_width / 2),
                                    rect.top() - (border_width / 2),
                                    rect.width() + border_width,
                                    rect.height() + border_width)
        path = PySide2.QtGui.QPainterPath()
        path.addRoundedRect(border_rect, radius+4, radius+4)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(PySide2.QtGui.QPen(border_color, border_width))
        painter.drawPath(path)

        painter.restore()

    def foldNode(self):
        self.isExtended = False
        self._height = 33
        self._width = 180
        self.pubFileTable.hide()

        self.rightPort.setPos(self._width, 10.0)
        offset = self.widget_pubButton.size().width() + 8
        self.widget_pubButton.setPos(self._width - offset, 4)

        for edge in self.rightPort.adjacentList:
            edge.updateDraw()

    def unfoldNode(self):
        self.isExtended = True
        self._height = self.originHeight
        self._width = 350
        self.pubFileTable.show()

        self.rightPort.setPos(self._width, 10.0)
        offset = self.widget_pubButton.size().width() + 8
        self.widget_pubButton.setPos(self._width - offset, 4)

        for edge in self.rightPort.adjacentList:
            edge.updateDraw()

    def mouseDoubleClickEvent(self, event):
        if self.isExtended:
            self.foldNode()

        else:
            self.unfoldNode()

        self.nodeScene.update()

        super(Node, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        for edge in self.leftPort.adjacentList:
            edge.updateDraw()

        for edge in self.rightPort.adjacentList:
            edge.updateDraw()

        super(Node, self).mouseMoveEvent(event)

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange and self.nodeScene:
            self.setZValue(2)
            if not self.isSelected():
                self.setZValue(3)

        return super(Node, self).itemChange(change, value)

    def getLeftNodes(self):
        nodes = []
        for edge in self.leftPort.adjacentList:
            nodes.append(edge.leftNode)
        return nodes

    def getRightNodes(self):
        nodes = []
        for edge in self.rightPort.adjacentList:
            nodes.append(edge.rightNode)
        return nodes

    def _pubButtonHandle(self):
        # Start on arrow animation of output pipe
        for edge in self.rightPort.adjacentList:
            edge.startArrowAnimation()

    def findLeftNodeById(self, _id):
        for edge in self.leftPort.adjacentList:
            if edge.leftNode._id == _id:
                return edge.leftNode
        return None

    def findRightNodeById(self, _id):
        for edge in self.rightPort.adjacentList:
            if edge.rightNode._id == _id:
                return edge.rightNode
        return None

    def deleteNode(self):
        for edge in self.leftPort.adjacentList:
            edge.leftPort.adjacentList.remove(edge)
            self.nodeScene.removeItem(edge)
        
        for edge in self.rightPort.adjacentList:
            edge.endPort.adjacentList.remove(edge)
            self.nodeScene.removeItem(edge)

        self.nodeScene.removeItem(self)

    @property
    def sceneWidget(self):
        return self.scene().parent()

    @property
    def nodeScene(self):
        return self.scene()
        

