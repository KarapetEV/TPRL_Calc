import sys
from PyQt5.QtWidgets import QApplication, QLabel, QSplashScreen
from PyQt5.QtGui import QMovie, QPixmap


class Splash(QSplashScreen):

    def __init__(self):
        super(Splash, self).__init__()
        self.setFixedSize(500, 400)
        self.setPixmap(QPixmap("img/splash_img.jpg"))

        self.label_title = QLabel(self)
        self.label_title.setGeometry(0, 30, 500, 100)
        self.label_title.setPixmap(QPixmap("img/splash_appname.png"))
        self.label_msg = QLabel(self)
        self.label_msg.setGeometry(200, 150, 100, 100)
        self.label_msg.setText("Скоро поедем...")
        self.label_animation = QLabel(self)
        self.label_animation.setGeometry(200, 250, 100, 100)
        self.movie = QMovie("img/load1.gif")
        self.label_animation.setScaledContents(True)
        self.label_animation.setMovie(self.movie)
        self.movie.start()