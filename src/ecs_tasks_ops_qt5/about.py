# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class UiAboutDialog(object):
    """Widget class for about dialog."""

    def setupUi(self, about_dialog):
        """Setup UI widgets."""
        about_dialog.setObjectName("about_dialog")
        about_dialog.resize(403, 246)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(about_dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout")
        self.app_name = QtWidgets.QLabel(about_dialog)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.app_name.setFont(font)
        self.app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name.setObjectName("app_name")
        self.vertical_layout.addWidget(self.app_name)
        self.author = QtWidgets.QLabel(about_dialog)
        self.author.setAlignment(QtCore.Qt.AlignCenter)
        self.author.setObjectName("author")
        self.vertical_layout.addWidget(self.author)
        self.help = QtWidgets.QLabel(about_dialog)
        self.help.setTextFormat(QtCore.Qt.MarkdownText)
        self.help.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.help.setWordWrap(True)
        self.help.setObjectName("help")
        self.vertical_layout.addWidget(self.help)
        self.version = QtWidgets.QLabel(about_dialog)
        self.version.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.version.setObjectName("version")
        self.vertical_layout.addWidget(self.version)
        self.button_box = QtWidgets.QDialogButtonBox(about_dialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.button_box.setObjectName("button_box")
        self.vertical_layout.addWidget(self.button_box)
        self.verticalLayout_2.addLayout(self.vertical_layout)

        self.retranslateUi(about_dialog)
        self.button_box.accepted.connect(about_dialog.accept)
        self.button_box.rejected.connect(about_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(about_dialog)

    def retranslateUi(self, about_dialog):
        """Translate widgets."""
        _translate = QtCore.QCoreApplication.translate
        about_dialog.setWindowTitle(_translate("about_dialog", "Dialog"))
        self.app_name.setText(_translate("about_dialog", "ECS Tasks Operations"))
        self.author.setText(
            _translate("about_dialog", "Pablo Palazon <ppalazon@antara.ws>")
        )
        self.help.setText(
            _translate(
                "about_dialog",
                '<html><head/><body><p>This application will let you access through SSH to your ECS resources such as containers instances and docker containers. It will also allow you to stop tasks and restart services. </p><p><span style=" font-weight:600;">This is not a replacement of ECS User interface</span></p></body></html>',
            )
        )
        self.version.setText(_translate("about_dialog", "Version: 0.1.0 "))
