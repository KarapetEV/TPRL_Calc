# -*- coding: utf-8 -*-

# © Copyright 2021 Aleksey Karapyshev, Evgeniy Karapyshev
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

# This file is part of TPRL Calculator.
#
#     TPRL Calculator is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <https://www.gnu.org/licenses/>.


import os
import numpy as np
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
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
        ax.set_theta_direction(-1)
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
        self.layout.addWidget(plotWidget, Qt.AlignVCenter)

    def save_chart(self, dir, file_name):
        self.figure.savefig(f".\{dir}\\{file_name}.png", dpi=300)
