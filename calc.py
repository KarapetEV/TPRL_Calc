# Тут будет крутой калькулятор
from PyQt5 import QtCore, QtWidgets, uic, QtGui

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("firstForm.ui", self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('rjd.png'))
    # window.resize(300,70)
    window.show()
    sys.exit(app.exec_())