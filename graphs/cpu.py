#!/usr/bin/env python3

# gpu.py - Graph various cpu values on a single chart

import sys
from random import randint

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg

from hwutils import CpuData

CPUDATA = CpuData()
VOLTAGEMODIFER = 1000
TEMPMODIFER = 67
TYPES = ["Voltage", "Max Clock", "Average Clock", "Average Temp"]

VALUES = [
    round(CPUDATA.voltage * VOLTAGEMODIFER),
    CPUDATA.max_clock,
    CPUDATA.average_clock,
    round(CPUDATA.average_temp * 67),
]

for value in VALUES:
    print(value)

#         voltage      avg_clock   max_clock   avg_temp
#          Green      Turquoise    Blueish     Red

COLORS = ["#6fb126", "#1B8B84", "#04A5C4", "#e61779"]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # TODO - Initialize the graph with relevant data points
        self.x = list(range(200))  # 100 time points
        self.y = [randint(0, 0) for _ in range(200)]  # 100 data points

        self.y_values = []
        for _value in VALUES:
            self.y_values.append([randint(0, 0) for _ in range(200)])

        # self.y2 = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground("black")
        self.graphWidget.setYRange(300, 5500, padding=0)
        self.graphWidget.setLabel("bottom", "Time", units="s")
        self.graphWidget.showGrid(x=False, y=True)

        self.pens = [pg.mkPen(color=color) for color in COLORS]

        self.lines = []

        for index, _value in enumerate(VALUES):
            self.graphWidget.addLegend()
            self.lines.append(
                self.graphWidget.plot(self.x, self.y, name=TYPES[index], pen=self.pens[index])
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
        for index, value in enumerate(FANS):
            if value.name == object_name:
                self.pens[index] = pg.mkPen(color=color)
        self._pen = pg.mkPen(color=color)

    @property
    def new_value(self):
        CPUDATA = CpuData()
        new_values = [
            round(CPUDATA.voltage * VOLTAGEMODIFER),
            CPUDATA.max_clock,
            CPUDATA.average_clock,
            round(CPUDATA.average_temp * 67),
        ]
        return new_values

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


app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
