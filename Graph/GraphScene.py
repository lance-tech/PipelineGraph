import PySide2
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
from Graph.ConnectablePort import ConnectablePort
from Graph.Edge import Edge
from Graph.Node import Node
from Graph import NodeUtil


class GraphScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent=None):
        super(GraphScene, self).__init__(parent)
        self.setObjectName('GraphScene')

        self.edgeList = []
        self.tempEdge = None
        self.selectedEdge = None
        self.selectedNode = None

        textItem = self.addText("(0, 0)", PySide2.QtGui.QFont("Times", 10, PySide2.QtGui.QFont.Bold))
        textItem.setPos(-20, -20)

    def destroy(self):
        self.sceneWidget.sceneList.remove(self)

    def drawGrid(self, painter, rect, pen, grid_size):
        lines = []
        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        x = left
        while x < rect.right():
            x += grid_size
            lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
        y = top
        while y < rect.bottom():
            y += grid_size
            lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
        painter.setPen(pen)
        painter.drawLines(lines)

    def drawBackground(self, painter, rect):
        painter.save()

        color = PySide2.QtGui.QColor(60, 60, 60)
        painter.setRenderHint(PySide2.QtGui.QPainter.Antialiasing, False)
        painter.setBrush(color)
        painter.drawRect(rect.normalized())
        grid_size = 20
        zoom = 0
        color = PySide2.QtGui.QColor(40, 40, 40)
        if zoom > -4:
            pen = PySide2.QtGui.QPen(color, 0.65)
            self.drawGrid(painter, rect, pen, grid_size)

        color = color.darker(150)
        pen = PySide2.QtGui.QPen(color, 0.65)
        self.drawGrid(painter, rect, pen, grid_size * 8)

        painter.restore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            if self.selectedNode:
                self.selectedNode.deleteNode()
                self.selectedNode = None

            if self.selectedEdge:
                self.selectedEdge.disconnect()
                self.selectedEdge = None

    def mousePressEvent(self, event):
        pos = event.scenePos()

        _item = self.itemAt(pos, self.viewer.transform())
        if isinstance(_item, ConnectablePort):
            self.tempEdge = Edge(_item)
            self.edgeList.append(self.tempEdge)
            self.addItem(self.tempEdge)

        if isinstance(_item, Node):
            self.selectedNode = _item
        else:
            self.selectedNode = None

        if isinstance(_item, Edge):
            self.selectedEdge = _item
        else:
            self.selectedEdge = None

        super(GraphScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.scenePos()

        if self.tempEdge:
            self.tempEdge.updateDraw(pos)

        super(GraphScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos = event.scenePos()

        destinationPort = self.itemAt(pos, self.viewer.transform())
        if self.tempEdge and self.isCanConnect(destinationPort):
            self.connectEdge(destinationPort)
        else:
            self.tempEdge = None
        super(GraphScene, self).mouseReleaseEvent(event)

    def isCanConnect(self, destinationPort):
        # Check is can connect if not return 
        if not isinstance(destinationPort, ConnectablePort):
            self.tempEdge.removeEdge()
            self.edgeList.remove(self.tempEdge)
            return False

        if destinationPort.port_type != NodeUtil.LEFT_PORT:
            self.tempEdge.removeEdge()
            self.edgeList.remove(self.tempEdge)
            return False

        if self.tempEdge.leftPort.port_type != NodeUtil.RIGHT_PORT:
            self.tempEdge.removeEdge()
            self.edgeList.remove(self.tempEdge)
            return False

        if not destinationPort.isLeftEdge(self.tempEdge.leftNode):
            self.tempEdge.removeEdge()
            self.edgeList.remove(self.tempEdge)
            return False

        if self.tempEdge.leftNode == destinationPort.parentItem():
            self.tempEdge.removeEdge()
            self.edgeList.remove(self.tempEdge)
            return False
        return True

    def connectEdge(self, destinationPort):
        # Connect pipe input node with output node
        self.tempEdge.setRightPort(destinationPort)
        self.tempEdge = None

    def findNodeById(self, id):
        for node in self.items():
            if isinstance(node, Node):
                if node._id == id:
                    return node
        return None

    @property
    def viewer(self):
        return self.views()[0] if self.views() else None

    @property
    def sceneWidget(self):
        return self.parent()
                

