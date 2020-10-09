"""Qt5 Gui for ECS tasks ops."""

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QLabel("This is a PyQt5 window!")

        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)


def main_gui():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
