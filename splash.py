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

from PyQt5.QtWidgets import QLabel, QSplashScreen
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt


class Splash(QSplashScreen):

    def __init__(self):
        super(Splash, self).__init__()
        self.setFixedSize(500, 400)
        self.setPixmap(QPixmap("img/splash_img.jpg"))

        self.label_title = QLabel(self)
        self.label_title.setGeometry(0, 30, 500, 100)
        self.label_title.setPixmap(QPixmap("img/splash_appname.png"))
        self.label_msg = QLabel(self)
        self.label_msg.setGeometry(150, 150, 200, 100)
        self.label_msg.setText("Загрузка компонентов интерфейса...")
        self.label_msg.setAlignment(Qt.AlignCenter)
        self.label_animation = QLabel(self)
        self.label_animation.setGeometry(200, 250, 100, 100)
        self.movie = QMovie("img/load1.gif")
        self.label_animation.setScaledContents(True)
        self.label_animation.setMovie(self.movie)
        self.movie.start()