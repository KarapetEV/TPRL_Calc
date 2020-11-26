import sys
from calc_window import *
from PyQt5 import QtCore, QtWidgets, uic, QtGui


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_AppWindow()
        self.ui.setupUi(self)
        self.ui.ugtSlider.valueChanged.connect(self.change_ugt_level)

    def change_ugt_level(self):
        labels_ugt = {
            self.ui.label_ugt0: 0,
            self.ui.label_ugt1: 1,
            self.ui.label_ugt2: 2,
            self.ui.label_ugt3: 3,
            self.ui.label_ugt4: 4,
            self.ui.label_ugt5: 5,
            self.ui.label_ugt6: 6,
            self.ui.label_ugt7: 7,
            self.ui.label_ugt8: 8,
            self.ui.label_ugt9: 9,
        }
        size = self.ui.ugtSlider.value()
        for k, v in labels_ugt.items():
            font = QtGui.QFont()
            if v == size:
                font.setPointSize(16)
                k.setFont(font)
                k.setEnabled(True)
            else:
                font.setPointSize(12)
                k.setFont(font)
                k.setEnabled(False)

        self.setupUi(self)
        self.set_params.clicked.connect(self.on_clicked)

    def on_clicked(self):
        text = self.set_params.text()
        if text == "Установить параметры":
            self.set_params.setText("Параметры установлены")
        else:
            self.set_params.setText("Установить параметры")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('rjd.png'))
    window.show()
    sys.exit(app.exec_())