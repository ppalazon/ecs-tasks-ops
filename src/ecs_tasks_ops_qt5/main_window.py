# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class UiMainWindow(object):
    """Widget composition for application."""

    def setupUi(self, main_window):
        """Inialization."""
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_horizontal = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_horizontal.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_horizontal.setObjectName("splitter_horizontal")
        self.splitter_vertical = QtWidgets.QSplitter(self.splitter_horizontal)
        self.splitter_vertical.setOrientation(QtCore.Qt.Vertical)
        self.splitter_vertical.setObjectName("splitter_vertical")
        self.ecs_elements = ECSElementsTreeWidget(self.splitter_vertical)
        self.ecs_elements.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ecs_elements.setIndentation(12)
        self.ecs_elements.setObjectName("ecs_elements")
        self.attributes = ECSAttributesTreeWidget(self.splitter_vertical)
        self.attributes.setObjectName("attributes")
        self.tabWidget = ECSTabView(self.splitter_horizontal)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.splitter_horizontal)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menu_ecs_taks_ops = QtWidgets.QMenu(self.menubar)
        self.menu_ecs_taks_ops.setObjectName("menu_ecs_taks_ops")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.action_about = QtWidgets.QAction(main_window)
        self.action_about.setObjectName("action_about")
        self.action_quit = QtWidgets.QAction(main_window)
        self.action_quit.setObjectName("action_quit")
        self.action_reload_clusters = QtWidgets.QAction(main_window)
        self.action_reload_clusters.setObjectName("action_reload_clusters")
        self.action_reload_config = QtWidgets.QAction(main_window)
        self.action_reload_config.setObjectName("action_reload_config")
        self.menu_ecs_taks_ops.addAction(self.action_about)
        self.menu_file.addAction(self.action_reload_config)
        self.menu_file.addAction(self.action_reload_clusters)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_ecs_taks_ops.menuAction())

        self.retranslateUi(main_window)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        """Translate widget."""
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.ecs_elements.headerItem().setText(
            0, _translate("main_window", "ECS Elements")
        )
        self.attributes.headerItem().setText(0, _translate("main_window", "Name"))
        self.attributes.headerItem().setText(1, _translate("main_window", "Value"))
        self.menu_ecs_taks_ops.setTitle(_translate("main_window", "Help"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.action_about.setText(_translate("main_window", "About"))
        self.action_about.setShortcut(_translate("main_window", "Ctrl+A"))
        self.action_quit.setText(_translate("main_window", "Quit"))
        self.action_quit.setShortcut(_translate("main_window", "Ctrl+Q"))
        self.action_reload_clusters.setText(
            _translate("main_window", "Reload Clusters")
        )
        self.action_reload_clusters.setShortcut(_translate("main_window", "Ctrl+R"))
        self.action_reload_config.setText(_translate("main_window", "Reload Config"))


from ecs_tasks_ops_qt5.qt5_ecs import (
    ECSAttributesTreeWidget,
    ECSElementsTreeWidget,
    ECSTabView,
)
