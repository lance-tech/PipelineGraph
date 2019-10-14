# Pipeline Graph
Visualization to publish state working flow in VFX Production.

## Build on
- Python 3.7
- PySide2



## Introduction
Works on the principle of basic graph algorithm.

A single node has two input/output connections.

The port entering the input based on the location of the plug is specified as the **Left Port**, and the port leaving the output as the **Right Port**.

A number of adjacent nodes can be connected to each port.
  
## Useage
When creating a node, the type must be specified.
The node type is defined as Enum Class in the ***Graph/NodeUtil.py*** file.

Each node can be connected by an edge.
The first argument passes the node that connects to the left side of the edge, and the second argument that connects to the right side of the edge.

Adjacent nodes are included in the port class as a list.


Below is an example of creating a simple node and you can run ***example.py*** to see it right away.
  
```python
node1 = Node(NodeUtil.NODE_TYPE.mod, _id=1)
node1.setPos(-100, 10)
scene.addItem(node1)

node2 = Node(NodeUtil.NODE_TYPE.rig, _id=2)
node2.setPos(200, 0)
scene.addItem(node2)

edge1 = Edge(node1.rightPort, node2.leftPort)
scene.addItem(edge1)
```
