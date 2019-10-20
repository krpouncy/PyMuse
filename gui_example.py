from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QGridLayout, QPushButton)
from PyQt5.QtCore import QThread, QObject, Qt
from PyQt5.QtGui import QFont
import PyMuse
import sys
import math


class MainProgram(QWidget):
    def __init__(self):
        super().__init__()
        # variable for server thread to start and stop
        self.server_thread = None
        # variable of PyMuse Headband child class to pass variables to
        self.brainreader = None
        # variables to hold UI Labels
        self.brainwave_labels = {}
        # draw the UI
        self.init_UI()

    def label(self, str, size=24):
        label = QLabel(str, self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('SansSerif', size))
        return label

    def start_server_thread(self):
        if self.server_thread and self.brainwave_labels != {}:
            self.brainreader.brainwave_labels = self.brainwave_labels
            self.server_thread.start()

    def stop_server_thread(self):
        # stop the server
        self.brainreader.stop()
        # end the thread
        self.server_thread.quit()

    def init_UI(self):
        # create a label for each brainwave
        brainwaves = ["alpha", "theta", "delta", "beta", "gamma"]
        for bw in brainwaves:
            # create four labels for each brainwave and add to dictionary
            labels = []
            for i in range(4):
                labels.append(self.label("0.000", size=16))
            self.brainwave_labels[bw] = labels

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # create the button and add to grid layout
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_server_thread)
        self.start_button.resize(self.start_button.sizeHint())
        self.start_button.setToolTip(
            "Enter the Server IP Before Pressing This")
        grid_layout.addWidget(self.start_button, 0, 0)

        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stop_server_thread)
        stop_button.resize(stop_button.sizeHint())
        grid_layout.addWidget(stop_button, 0, 1)

        # add the labels to the grid
        grid_column, grid_row = 0, 1
        for key in sorted(self.brainwave_labels):
            # create a the title label and add to grid
            grid_column = 0
            title_label = self.label(key, size=20)
            grid_layout.addWidget(title_label, grid_row, grid_column)
            # add the brain labels to the grid
            grid_column = 1
            for i in self.brainwave_labels[key]:
                grid_layout.addWidget(i, grid_row, grid_column)
                grid_column += 1
            grid_row += 1

        # self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle("GUI Example")
        self.show()

# the child class also extends QObject to operate on seperate thread


class BrainReader(QObject, PyMuse.Headband):
    # create label variables
    brainwave_labels = {}

    def __init__(self, **kwargs):
        # call the __init__ of parent classes
        QObject.__init__(self)
        PyMuse.Headband.__init__(self, **kwargs)

    def run(self):
        brainwaves = self.get_brainwaves()
        if brainwaves != {}:
            # set the text
            for bw in sorted(brainwaves):
                for i in range(4):
                    val = round(brainwaves[bw][i], 3)
                    self.brainwave_labels[bw][i].setText(str(val))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainprogram = MainProgram()

    ip = input("[~] Enter computer IP address:")
    brainreader = BrainReader(ip = ip, port = 5000)
    print("[!] ip and port set.. ready")

    # create the thread
    objThread = QThread()
    brainreader.moveToThread(objThread)
    objThread.started.connect(brainreader.start_server)

    # add to the main progam
    mainprogram.server_thread = objThread
    mainprogram.brainreader = brainreader

    sys.exit(app.exec_())
