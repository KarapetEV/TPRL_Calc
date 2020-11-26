# Тут будет крутой калькулятор
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import ui_firstForm

class Window(QtWidgets.QWidget, ui_firstForm.Ui_FormParams):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('rjd.png'))
    window.show()
    sys.exit(app.exec_())