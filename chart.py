# -*- coding: utf-8 -*-

# Copyright 2020 Aleksey Karapyshev, Evgeniy Karapyshev ©
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>


import os
import numpy as np
from PyQt5 import QtCore, QtWidgets, uic
import matplotlib
import matplotlib.pyplot as plt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Chart:

    num = 0

    def __init__(self, data, lay):
        self.data = data
        self.layout = lay
        self.figure = None
        self.create_chart()

    def create_chart(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        params = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']
        results = []
        for el in params:
            results.append(float(self.data[el]))

        results = np.append(results, results[0])
        self.figure = plt.figure(figsize=(12, 12), facecolor='#f3f3f3')
        plt.subplot(polar=True)
        theta = np.linspace(start=0, stop=2 * np.pi, num=len(results))
        ax = self.figure.add_subplot(111, projection='polar')
        ax.set(facecolor='#f3f3f3')
        ax.set_theta_offset(np.pi / 2)
        ax.set_ylim(0, 9)
        ax.set_yticks(np.arange(0, 10, 1.0))
        plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], fontsize=6, color='grey')
        ax.set_rlabel_position(0)
        gridlines = ax.yaxis.get_gridlines()
        for gl in gridlines:
            gl.get_path()._interpolation_steps = 5
        plt.box(on=None)
        lines, labels = plt.thetagrids(range(0, 360, int(360 / len(params))), (params))
        plt.plot(theta, results)
        plt.fill(theta, results, 'b', alpha=0.1)
        plotWidget = FigureCanvas(self.figure)
        self.layout.addWidget(plotWidget, QtCore.Qt.AlignVCenter)

    def save_chart(self, num):
        if not os.path.isdir("Charts"):
            os.mkdir("Charts")
        self.figure.savefig(f".\Charts\\{num}_chart.png", dpi=300)
