#!/usr/bin/env python3

# temp_graph.py - Graph temp speeds on a single chart

import sys
import subprocess
from random import randint

from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QToolBar
from PySide6.QtCore import QTimer
import pyqtgraph as pg

from RandomRgb import generate_rgb

from hwdata.CPU import CpuData
from hwdata.GPU import GpuData
from hwdata.SYS import SystemTemp

from ExecutionTimer import ExecutionTimer

TEMPS = [CpuData(), GpuData(), SystemTemp()]
#       CPU,          GPU,           SYS
#       Magenta,   Green,        Orange
COLORS = ["#880cbc", "#6fb126", "#aa9001"]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # TODO - Initialize the graph with relevant data points
        self.x = list(range(200))  # 100 time points
        self.y = [randint(0, 0) for _ in range(200)]  # 100 data points

        self.y_values = []
        for temp in TEMPS:
            self.y_values.append([randint(0, 0) for _ in range(200)])

        # self.y2 = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground("black")
        self.graphWidget.setYRange(0, 100, padding=0)
        self.graphWidget.setLabel("left", "Temperature", units="C")
        self.graphWidget.setLabel("bottom", "Time", units="s")
        self.graphWidget.showGrid(x=False, y=True)
        self.pens = [pg.mkPen(color=color) for color in COLORS]
        self.setCentralWidget(self.graphWidget)
        self.addToolBar(QToolBar("TEST"))
        self.lines = []

        # Initialize the lines and add them to the legend.
        # * Add current value to legend

        for index, temp in enumerate(TEMPS):
            self.graphWidget.addLegend()
            self.lines.append(
                self.graphWidget.plot(self.x, self.y, name=temp.type, pen=self.pens[index])
            )

        # self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        # self.data_line2 =  self.graphWidget.plot(self.x, self.y2, pen=pen2)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    @property
    def new_value(self):
        new_temps = [CpuData(), GpuData(), SystemTemp()]
        temps = []
        for temp in new_temps:
            temps.append(int(temp.temp))
        return temps

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        new_values = self.new_value
        for index, _y in enumerate(self.y_values):
            self.y_values[index] = self.y_values[index][1:]  # Remove the first
            self.y_values[index].append(new_values[index])
            self.lines[index].setData(self.x, self.y_values[index])

        # Update legend to show the new values

    def line_color(self, index, rgb):
        if rgb:
            return rgb
        else:
            return generate_rgb()

        # self.y = self.y[1:]  # Remove the first
        # new_values = self.new_value
        # self.y.append(new_values[0])  # Add a new random value.
        # self.y.append(new_values[1])
        # self.y.append(self.new_value[0])  # Add a new random value.
        # self.y2.append(self.new_value[1])

        # self.data_line.setData(self.x, self.y)  # Update the data.

        # self.data_line2.setData(self.x, self.y2)  # Update the data.


app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
