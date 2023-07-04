"""Terminal emulation with xterm.js."""
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebChannel
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWidgets

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TerminalProcess(QtCore.QProcess):
    """Terminal process."""

    data_changed = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        """Init terminal process."""
        super().__init__(parent)

        self.readyRead.connect(self._handle_ready_read)
        self.error.connect(self._handle_error)
        self.stateChanged.connect(self.handle_state)
        self.setProcessChannelMode(
            QtCore.QProcess.MergedChannels
        )  # Error and output in the same channel
        # self.setProgram(command)
        # self.setArguments(args)
        # self.start()
        # self.waitForStarted()
        # self.readyReadStandardOutput.connect(self.handle_stdout)
        # self.readyReadStandardError.connect(self.handle_stderr)

    @QtCore.pyqtSlot(str)
    def send_data(self, message):
        """Write on terminal."""
        data = message.encode("utf8")
        # print(f"Write in process: {data}")
        self.write(data)

    def _handle_ready_read(self):
        """Write on xterm.js terminal."""
        data = self.readAll().data().replace(b"\n", b"\r\n")
        # print(f"Read from terminal: {data}")
        self.data_changed.emit(data.decode("utf8"))

    def _handle_error(self):
        """Show error on terminal."""
        print(f"Terminal error: {self.errorString()}")

    # def handle_stderr(self):
    #     data = self.p.readAllStandardError()
    #     stderr = bytes(data).decode("utf8")
    #     print(stderr)

    # def handle_stdout(self):
    #     data = self.p.readAllStandardOutput()
    #     stdout = bytes(data).decode("utf8")
    #     print(stdout)

    def handle_state(self, state):
        """Log status of terminal."""
        states = {
            QtCore.QProcess.NotRunning: "Not running",
            QtCore.QProcess.Starting: "Starting",
            QtCore.QProcess.Running: "Running",
        }
        state_name = states[state]
        process_id = self.processId()
        print(f"State changed: {state_name} for {process_id}")
        # if (state == QtCore.QProcess.NotRunning):
        #     super().close()


class ResizeListener(QtCore.QObject):
    """Resize listener to adapt xterm.js."""

    resized = QtCore.pyqtSignal()

    def __init__(self, widget):
        """Init resize listener."""
        super().__init__(widget)
        self._widget = widget
        if isinstance(self.widget, QtWidgets.QWidget):
            self.widget.installEventFilter(self)

    @property
    def widget(self):
        """Get widget associated with this listener."""
        return self._widget

    def eventFilter(self, obj, event):
        """Filter event to process resize."""
        if obj is self.widget and event.type() == QtCore.QEvent.Resize:
            QtCore.QTimer.singleShot(100, self.resized.emit)
        return super().eventFilter(obj, event)


class OpenBrowserUrl(QtCore.QObject):
    """Open on browser any link on xterm.js."""

    open_signal = QtCore.pyqtSignal(str)

    def __init__(self, widget):
        """Init url opener."""
        super().__init__(widget)
        self._widget = widget

    @property
    def widget(self):
        """Get widget associated with this listener."""
        return self._widget

    @QtCore.pyqtSlot(str)
    def open(self, url):
        """Process request to open url."""
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


class TerminalWidget(QtWebEngineWidgets.QWebEngineView):
    """WebEngine view associated with a terminal."""

    def __init__(self, parent=None):
        """Init webengine with xterm.js."""
        super().__init__(parent)

        resize_listener = ResizeListener(self)
        open_browser_url = OpenBrowserUrl(self)
        self.process = TerminalProcess(self)
        self.channel = QtWebChannel.QWebChannel(self)
        self.page().setWebChannel(self.channel)
        self.page().settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.JavascriptCanAccessClipboard, True
        )
        self.page().settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.JavascriptCanPaste, True
        )
        self.page().settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False
        )
        # self.page().setLinkDelegationPolicy(QtWebEngineWidgets.QWebPage.DelegateAllLinks)
        self.channel.registerObject("resize_listener", resize_listener)
        self.channel.registerObject("open_browser_url", open_browser_url)
        self.channel.registerObject("process", self.process)
        # self.channel.registerObject("socket", self.socket)
        filename = os.path.join(CURRENT_DIR, "terminal.html")
        self.page().load(QtCore.QUrl.fromLocalFile(filename))

    def start(self, command, args):
        """Execute process with xterm.js terminal."""
        self.process.start(command, args)

    def closeEvent(self, event):
        """Close terminal and process."""
        self.process.terminate()


# def main():
#     import sys

#     app = QtWidgets.QApplication(sys.argv)

#     QtCore.QCoreApplication.setApplicationName("QTermWidget Test")
#     QtCore.QCoreApplication.setApplicationVersion("1.0")

#     parser = QtCore.QCommandLineParser()
#     parser.addHelpOption()
#     parser.addVersionOption()
#     parser.setApplicationDescription(
#         "Example(client-side) for remote terminal of QTermWidget"
#     )

#     parser.process(QtCore.QCoreApplication.arguments())

#     requiredArguments = parser.positionalArguments()
#     # if len(requiredArguments) != 2:
#     #     parser.showHelp(1)
#     #     sys.exit(-1)
#     # address, port = requiredArguments

#     w = QtWidgets.QWidget()
#     layout = QtWidgets.QVBoxLayout(w)
#     for i in range(2):
#         wt = TerminalWidget()
#         wt.process.start("/bin/bash", ["--norc", "-i"]) # It doesn't work and I can't figure out why this happens
#         # wt.process.start("/bin/fish", ["-i"])
#         wt.process.waitForStarted()
#         wt.process.setProcessEnvironment(QtCore.QProcessEnvironment())
#         wt.process.write(b"set -o emacs\n")
#         print(f"Started {wt.process.processId()}")
#         layout.addWidget(wt)

#     w.resize(640, 480)
#     w.show()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
