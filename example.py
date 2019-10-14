import sys
import os
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets

import Graph.NodeUtil as NodeUtil
from Graph.GraphScene import GraphScene
from Graph.GraphView import GraphViewer
from Graph.Node import Node
from Graph.Edge import Edge


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = QtWidgets.QWidget()
    win.setWindowTitle('Graph Window')
    layout = QtWidgets.QGridLayout()
    win.setLayout(layout)

    scene = GraphScene()
    nodeViewer = GraphViewer(scene)
    layout.addWidget(nodeViewer)
    win.show()

    node1 = Node(NodeUtil.NODE_TYPE.mod, _id=1)
    node1.setPos(-100, 10)
    scene.addItem(node1)

    node2 = Node(NodeUtil.NODE_TYPE.rig, _id=2)
    node2.setPos(200, 0)
    scene.addItem(node2)

    node3 = Node(NodeUtil.NODE_TYPE.ani, _id=3)
    node3.setPos(200, 100)
    scene.addItem(node3)

    node4 = Node(NodeUtil.NODE_TYPE.cmp, _id=4)
    node4.setPos(200, 200)
    scene.addItem(node4)
    
    #node1 = scene.findNodeById(1)
    #node2 = scene.findNodeById(2)

    edge1 = Edge(node1.rightPort, node2.leftPort)
    scene.addItem(edge1)

    sys.exit(app.exec_())