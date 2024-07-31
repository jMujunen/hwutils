#!/usr/bin/env python3

# fan_graph.py - Graph fan speeds on a single chart

import graphs

import sys
import subprocess
from random import randint

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg

from hwdata.CPU import CpuData
from hwdata.FAN import Fan
from hwdata.GPU import GpuData


FANS = [
    Fan("fan1", "CPU"),
    Fan("fan2", "REAR"),
    Fan("fan3", "SYS1"),
    Fan("fan4", "SYS2"),
    Fan("fan5", "SYS3"),
    Fan("fan6", "BOTTOM"),
    GpuData(),
]

#         CPU          REAR      SYS1        SYS2        SYS3       BOTTOM       GPU
#         Magenta     Redish   Turquoise   Turquoise   Turquoise                Green

COLORS = ["#880cbc", "#b12680", "#1B8B84", "#0ca0bc", "#0c82bc", "#a5a500", "#6fb126"]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # TODO - Initialize the graph with relevant data points
        self.x = list(range(200))  # 100 time points
        self.y = [randint(0, 0) for _ in range(200)]  # 100 data points

        self.y_values = []
        for fan in FANS:
            self.y_values.append([randint(0, 0) for _ in range(200)])

        # self.y2 = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground("black")
        self.graphWidget.setYRange(300, 1700, padding=0)
        self.graphWidget.setLabel("left", "Fan Speed RPM")
        self.graphWidget.setLabel("bottom", "Time", units="s")

        self.pens = [pg.mkPen(color=color) for color in COLORS]

        self.lines = []

        for index, fan in enumerate(FANS):
            self.graphWidget.addLegend()
            self.lines.append(
                self.graphWidget.plot(self.x, self.y, name=fan.type, pen=self.pens[index])
            )
        # self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        # self.data_line2 =  self.graphWidget.plot(self.x, self.y2, pen=pen2)

        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    @property
    def pen(self):
        return self._pen

    @pen.setter
    def pen(self, color, object_name):
        for index, fan in enumerate(FANS):
            if fan.name == object_name:
                self.pens[index] = pg.mkPen(color=color)
        self._pen = pg.mkPen(color=color)

    @property
    def new_value(self):
        speeds = []
        for fan in FANS:
            speeds.append(int(fan.speed))
        return speeds

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        new_values = self.new_value
        for index, _y in enumerate(self.y_values):
            self.y_values[index] = self.y_values[index][1:]  # Remove the first
            self.y_values[index].append(new_values[index])
            self.lines[index].setData(self.x, self.y_values[index])

        # self.y.append(self.new_value[0])  # Add a new random value.
        # self.y2.append(self.new_value[1])

        # self.data_line.setData(self.x, self.y)  # Update the data.

        # self.data_line2.setData(self.x, self.y2)  # Update the data.


def generate_rgb():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)


app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
