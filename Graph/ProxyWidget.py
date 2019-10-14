import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets


class ProxyWidgetToolButton(QtWidgets.QGraphicsProxyWidget):
    def __init__(self, parent=None, name=''):
        super(ProxyWidgetToolButton, self).__init__(parent)
        self.setZValue(4)
        self.widget = QtWidgets.QToolButton()
        self.widget.setObjectName('proxyWidgetTollButton')
        self.widget.setText(name)
        self.setWidget(self.widget)


class ProxyWidgetLabel(QtWidgets.QGraphicsProxyWidget):
    def __init__(self, parent=None, name=''):
        super(ProxyWidgetLabel, self).__init__(parent)
        self._name = name
        self.setZValue(4)
        self.widget = QtWidgets.QLabel(self._name)
        self.widget.setObjectName('proxyWidgetLabel')
        self.setWidget(self.widget)

    def setText(self, text):
        self.widget.setText(text)


class ProxyWidgetTable(QtWidgets.QGraphicsProxyWidget):
    def __init__(self, parent=None, title=''):
        super(ProxyWidgetTable, self).__init__(parent)
        self.setZValue(4)
        self._data = []
        self._user = {}

        _frame = QtWidgets.QFrame()
        _frame.resize(334, 150)
        _mainLayout = QtWidgets.QVBoxLayout()
        _mainLayout.setContentsMargins(0, 0, 0, 0)
        _frame.setLayout(_mainLayout)

        _header = QtWidgets.QWidget()
        _headerLayout = QtWidgets.QHBoxLayout()
        _headerLayout.setContentsMargins(6, 3, 6, 3)
        _header.setLayout(_headerLayout)

        _headLabel = QtWidgets.QLabel(title)
        _headerLayout.addWidget(_headLabel)

        self.widget = QtWidgets.QTableWidget(0, 3)
        _tableHeader = ['File Name', 'User', 'Date']
        self.widget.setHorizontalHeaderLabels(_tableHeader)
        self.widget.resizeColumnsToContents()
        self.widget.setColumnWidth(0, 220)
        self.widget.setColumnWidth(1, 50)
        header = self.widget.horizontalHeader()
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        _mainLayout.addWidget(_header)
        _mainLayout.addWidget(self.widget)

        self.right_menu = QtWidgets.QMenu(self.parent())
        self.remove_menu = self.right_menu.addAction("Remove")
        self.remove_menu.triggered.connect(self.remove_handle)
        self.clear_menu = self.right_menu.addAction("Clear")
        self.clear_menu.triggered.connect(self.clear_handle)
        self.widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.widget.customContextMenuRequested.connect(self._menu_handle)

        self.setWidget(_frame)

    @property
    def user(self):
        return self._user.keys()

    @property
    def data(self):
        return self._data

    def _menu_handle(self, s_pos):
        self.mouse_pos = s_pos
        self.right_menu.exec_(QtWidgets.QCursor.pos())

    def addFile(self, file_name, user=None, date=None):
        res = self.widget.findItems(file_name, QtCore.Qt.MatchContains)
        if len(res) > 0:
            # update file information
            itemRow = res[0].row()
            userItem = self.widget.item(itemRow, 1)
            dateItem = self.widget.item(itemRow, 2)

            userItem.setText(user)
            dateItem.setText(str(date))
            return itemRow

        index = self.widget.rowCount()
        self.widget.insertRow(index)
        self.widget.setItem(index, 0, QtWidgets.QTableWidgetItem(file_name))
        self.widget.setItem(index, 1, QtWidgets.QTableWidgetItem(user))
        self.widget.setItem(index, 2, QtWidgets.QTableWidgetItem(date))
        return -1
        
    def remove_handle(self):
        try:
            _t = self.widget.takeTopLevelItem(self.widget.indexAt(self.mouse_pos).row()).text(0)
        except:
            return
        if _t in (self.user):
            del self._user[_t]
        elif _t in self._user.values():
            del self._user[[k for k, v in self._user.items() if v == _t][0]]
        self._data.remove(_t)

    def clear_handle(self):
        self.widget.clear()
        self._user.clear()
        self._data = []
