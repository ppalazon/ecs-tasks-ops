"""Qt5 User Interface for ECS Tasks Ops"""

import sys
from PyQt5 import QtWidgets, uic

from ecs_tasks_ops_qt5.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


def main_gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()