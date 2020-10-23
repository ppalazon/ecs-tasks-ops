"""Qt5 User Interface for ECS Tasks Ops"""

import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui

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

        self.splitter_horizontal.setSizes([100, 200])
        self.splitter_vertical.setSizes([200, 100])
        self.ecs_elements.statusChanged.connect(self.statusbar.showMessage)


def main_gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main_gui()