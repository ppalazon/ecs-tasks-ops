"""Qt5 User Interface for ECS Tasks Ops"""

import sys
from PyQt5 import QtWidgets, uic, QtCore

from ecs_tasks_ops import ecs_data
from ecs_tasks_ops_qt5.MainWindow import Ui_MainWindow
from ecs_tasks_ops_qt5.qt5_ecs import ECSClusterTreeItem


class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.command = QtWidgets.QLineEdit(self)
        self.command.setReadOnly(True)
        self.command.setText("ssh i-2343432fds")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.command)
        layout.addWidget(self.terminal)

        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.terminal.winId()))])


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("ECS Tasks Operations")

        self.resizeSplitters()
        self.initialize_ecs_elements()     
        self.initialize_attributes()   


    def resizeSplitters(self):
        self.splitter_horizontal.setSizes([100, 200])
        self.splitter_vertical.setSizes([200, 100])

    
    def initialize_attributes(self):
        self.attributes.setColumnCount(2)
        self.attributes.setHeaderItem(QtWidgets.QTreeWidgetItem(["Name", "Value"]))


    def initialize_ecs_elements(self):
        self.ecs_elements.setColumnCount(2)
        self.ecs_elements.setHeaderItem(QtWidgets.QTreeWidgetItem(["Name", "arn"]))

        for cluster in ecs_data.get_clusters():
            self.ecs_elements.addTopLevelItem(ECSClusterTreeItem(cluster))

        self.ecs_elements.itemClicked.connect(lambda item: self.onselect_ecs_element(item))
        self.ecs_elements.itemDoubleClicked.connect(lambda item: item.refresh_children())

    def onselect_ecs_element(self, item):
        self.statusbar.showMessage(item.name)
        self.attributes.clear()
        for attr in item.get_attributes():
            self.attributes.addTopLevelItem(QtWidgets.QTreeWidgetItem([str(a) for a in attr]))


def main_gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main_gui()