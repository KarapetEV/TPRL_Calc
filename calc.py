# Тут будет крутой калькулятор
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import ui_firstForm

class Window(QtWidgets.QWidget, ui_firstForm.Ui_FormParams):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.set_params.clicked.connect(self.on_clicked)

    def on_clicked(self):
        text = self.set_params.text()
        if text == "Установить параметры":
            self.set_params.setText("Параметры установлены")
        else:
            self.set_params.setText("Установить параметры")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('rjd.png'))
    window.show()
    sys.exit(app.exec_())