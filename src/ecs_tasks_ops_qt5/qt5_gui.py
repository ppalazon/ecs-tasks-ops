"""Qt5 User Interface for ECS Tasks Ops"""

import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui

from ecs_tasks_ops import ecs_data
from ecs_tasks_ops_qt5.MainWindow import Ui_MainWindow
from ecs_tasks_ops_qt5.qt5_ecs import ECSClusterTreeItem

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("ECS Tasks Operations")

        self.splitter_horizontal.setSizes([100, 400])
        self.splitter_vertical.setSizes([200, 100])
        self.ecs_elements.statusChanged.connect(self.statusbar.showMessage)
        self.attributes.statusChanged.connect(self.statusbar.showMessage)

        self.actionQuit.triggered.connect(self.close)
        self.ecs_elements.currentItemChanged['QTreeWidgetItem*','QTreeWidgetItem*'].connect(self.attributes.update_attributes)
        self.actionReload_Clusters.triggered.connect(self.ecs_elements.reload_cluster_info)
        self.ecs_elements.commandShowDetail['QTreeWidgetItem*'].connect(self.tabWidget.show_detail)
        self.ecs_elements.commandContainerSSH['QTreeWidgetItem*'].connect(self.tabWidget.container_ssh)
        self.ecs_elements.commandTaskLog['QTreeWidgetItem*'].connect(self.tabWidget.task_log)
        self.ecs_elements.commandTaskStop['QTreeWidgetItem*'].connect(self.tabWidget.task_stop)
        self.ecs_elements.commandDockerLog['QTreeWidgetItem*'].connect(self.tabWidget.docker_container_log)
        self.ecs_elements.commandDockerExec['QTreeWidgetItem*'].connect(self.tabWidget.docker_container_exec)
        self.ecs_elements.commandServiceShowEvents['QTreeWidgetItem*'].connect(self.tabWidget.service_events)


def main_gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main_gui()