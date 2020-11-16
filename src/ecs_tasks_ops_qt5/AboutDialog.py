# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(403, 246)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.app_name = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.app_name.setFont(font)
        self.app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name.setObjectName("app_name")
        self.verticalLayout.addWidget(self.app_name)
        self.author = QtWidgets.QLabel(AboutDialog)
        self.author.setAlignment(QtCore.Qt.AlignCenter)
        self.author.setObjectName("author")
        self.verticalLayout.addWidget(self.author)
        self.help = QtWidgets.QLabel(AboutDialog)
        self.help.setTextFormat(QtCore.Qt.MarkdownText)
        self.help.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.help.setWordWrap(True)
        self.help.setObjectName("help")
        self.verticalLayout.addWidget(self.help)
        self.version = QtWidgets.QLabel(AboutDialog)
        self.version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.version.setObjectName("version")
        self.verticalLayout.addWidget(self.version)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Dialog"))
        self.app_name.setText(_translate("AboutDialog", "ECS Tasks Operations"))
        self.author.setText(_translate("AboutDialog", "Pablo Palazon <ppalazon@antara.ws>"))
        self.help.setText(_translate("AboutDialog", "<html><head/><body><p>This application will let you access through SSH to your ECS resources such as containers instances and docker containers. It will also allow you to stop tasks and restart services. </p><p><span style=\" font-weight:600;\">This is not a replacement of ECS User interface</span></p></body></html>"))
        self.version.setText(_translate("AboutDialog", "Version: 0.1.0 "))
