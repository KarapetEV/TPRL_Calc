# -*- coding: utf-8 -*-

import numpy as np
from PyQt5 import QtCore, QtWidgets, uic
import matplotlib
import matplotlib.pyplot as plt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_chart(data, frame):
    params = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']
    results = []
    for el in params:
        if el in data:
            results.append(float(data[el]))
        else:
            results.append(0.0)
    results = np.append(results, results[0])
    fig = plt.figure(figsize=(10, 10), facecolor='#f3f3f3')
    plt.subplot(polar=True)
    theta = np.linspace(start=0, stop=2*np.pi, num=len(results))
    ax = fig.add_subplot(111, projection='polar')
    ax.set(facecolor='#f3f3f3')
    ax.set_ylim(0, 9)
    ax.set_yticks(np.arange(0, 10, 1.0))
    lines, labels = plt.thetagrids(range(0, 360, int(360 / len(params))), (params))
    plt.plot(theta, results)
    plt.fill(theta, results, 'b', alpha=0.1)
    plotWidget = FigureCanvas(fig)
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(plotWidget, QtCore.Qt.AlignVCenter)

