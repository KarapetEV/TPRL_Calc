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

    label_placement = np.linspace(start=0.1*np.pi, stop=1.7*np.pi, num=len(results))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.set(facecolor='#f3f3f3')
    ax.set_ylim(0, 9)
    ax.set_yticks(np.arange(0, 9, 1.0))
    # plt.subplot(polar=True)
    lines, labels = plt.thetagrids(np.degrees(label_placement), labels=params)
    ax.plot(lines, labels)
    plotWidget = FigureCanvas(fig)
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(plotWidget, QtCore.Qt.AlignVCenter)

