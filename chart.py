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
    fig = plt.figure(figsize=(6, 6), facecolor='#f3f3f3')
    plt.subplot(polar=True)
    plt.plot(label_placement, results)
    lines, labels = plt.thetagrids(np.degrees(label_placement), labels=params)
    plotWidget = FigureCanvas(fig)
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(plotWidget)

    # arr = np.linspace(0, 2*np.pi, num=5)
    # print(label_placement)
    # print(np.degrees(label_placement))
