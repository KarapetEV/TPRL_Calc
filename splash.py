import sys
from PyQt5.QtWidgets import QApplication, QLabel, QSplashScreen
from PyQt5.QtGui import QMovie, QPixmap


class Splash(QSplashScreen):

    def __init__(self):
        super(Splash, self).__init__()
        self.setPixmap(QPixmap("img/splash_img.jpg"))

        self.label_title = QLabel(self)
        self.label_title.setGeometry(0, 20, 500, 100)
        self.label_title.setPixmap(QPixmap("img/splash_appname.png"))

        self.label_animation = QLabel(self)
        self.movie = QMovie("img/load1.gif")
        self.label_animation.setMovie(self.movie)
        self.movie.start()

app = QApplication(sys.argv)
splash = Splash()
splash.show()
sys.exit(app.exec_())