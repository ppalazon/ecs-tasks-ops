"""Qt5 User Interface for ECS Tasks Ops"""
import sys

import pkg_resources
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic

from ecs_tasks_ops import ecs_conf
from ecs_tasks_ops import ecs_data
from ecs_tasks_ops_qt5.AboutDialog import Ui_AboutDialog
from ecs_tasks_ops_qt5.MainWindow import Ui_MainWindow
from ecs_tasks_ops_qt5.qt5_ecs import ECSClusterTreeItem


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        version = pkg_resources.get_distribution("ecs_tasks_ops").version
        self.version.setText(f"Version: {version}")


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
        self.actionAbout.triggered.connect(self.open_about)
        self.ecs_elements.currentItemChanged[
            "QTreeWidgetItem*", "QTreeWidgetItem*"
        ].connect(self.attributes.update_attributes)
        self.actionReload_Clusters.triggered.connect(
            self.ecs_elements.reload_cluster_info
        )
        self.actionReload_Config.triggered.connect(self.reload_conf)
        self.ecs_elements.commandShowDetail["QTreeWidgetItem*"].connect(
            self.tabWidget.show_detail
        )
        self.ecs_elements.commandContainerSSH["QTreeWidgetItem*"].connect(
            self.tabWidget.container_ssh
        )
        self.ecs_elements.commandTaskLog["QTreeWidgetItem*"].connect(
            self.tabWidget.task_log
        )
        self.ecs_elements.commandTaskStop["QTreeWidgetItem*"].connect(
            self.tabWidget.task_stop
        )
        self.ecs_elements.commandDockerLog["QTreeWidgetItem*"].connect(
            self.tabWidget.docker_container_log
        )
        self.ecs_elements.commandDockerExec["QTreeWidgetItem*"].connect(
            self.tabWidget.docker_container_exec
        )
        self.ecs_elements.commandServiceShowEvents["QTreeWidgetItem*"].connect(
            self.tabWidget.service_events
        )
        self.ecs_elements.commandServiceRestart["QTreeWidgetItem*"].connect(
            self.tabWidget.service_restart
        )

    def open_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def reload_conf(self):
        ecs_conf.load_config()
        self.statusbar.showMessage("Reloading configuration")


def main_gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main_gui()
