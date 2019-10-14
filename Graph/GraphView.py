import PySide2
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets


class GraphViewer(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        super(GraphViewer, self).__init__(scene, parent)
        self.setObjectName('GraphViewer')
        self.setRenderHint(PySide2.QtGui.QPainter.Antialiasing, True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        scene_area = 8000.0
        scene_pos = (scene_area / 2) * -1
        self.setSceneRect(scene_pos, scene_pos, scene_area, scene_area)

        self.LMB_state = False
        self.RMB_state = False
        self.MMB_state = False

        self._origin_pos = None
        self._previous_pos = QtCore.QPoint(self.width(), self.height())

    def keyPressEvent(self, event):
        alt_modifier = event.modifiers() == QtCore.Qt.AltModifier
        if alt_modifier:
            QtWidgets.QApplication.setOverrideCursor(PySide2.QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        super(GraphViewer, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        super(GraphViewer, self).keyReleaseEvent(event)

    def mousePressEvent(self, event):
        self._origin_pos = event.pos()
        self._previous_pos = event.pos()

        if event.button() == QtCore.Qt.LeftButton:
            self.LMB_state = True

        super(GraphViewer, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        alt_modifier = event.modifiers() == QtCore.Qt.AltModifier
        if self.LMB_state and alt_modifier:
            pos_x = (event.x() - self._previous_pos.x())
            pos_y = (event.y() - self._previous_pos.y())
            self._set_viewer_pan(pos_x, pos_y)
        self._previous_pos = event.pos()
        super(GraphViewer, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.LMB_state = False
        super(GraphViewer, self).mouseReleaseEvent(event)

    def _set_viewer_pan(self, pos_x, pos_y):
        scroll_x = self.horizontalScrollBar()
        scroll_y = self.verticalScrollBar()
        scroll_x.setValue(scroll_x.value() - pos_x)
        scroll_y.setValue(scroll_y.value() - pos_y)

