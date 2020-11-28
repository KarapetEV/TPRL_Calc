import sys
import calc_window
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import pandas as pd


class Window(QtWidgets.QWidget, calc_window.Ui_AppWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.btn_set_params.clicked.connect(self.set_params)
        self.ugtSlider.valueChanged.connect(self.change_ugt_level)
        self.btn_calculate.clicked.connect(self.calculate)

    def change_ugt_level(self):
        labels_ugt = {
            self.label_ugt0: 0,
            self.label_ugt1: 1,
            self.label_ugt2: 2,
            self.label_ugt3: 3,
            self.label_ugt4: 4,
            self.label_ugt5: 5,
            self.label_ugt6: 6,
            self.label_ugt7: 7,
            self.label_ugt8: 8,
            self.label_ugt9: 9,
        }
        size = self.ugtSlider.value()
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

    def set_params(self):
        self.tabWidget.setCurrentIndex(1)
        self.get_params()
        self.frame_calc_params.setEnabled(False)

    def get_params(self):

        params = []
        rad = []
        tasks_list = []
        type = ''

        self.check_calc_trl.setChecked(self.check_trl.isChecked())
        self.check_calc_mrl.setChecked(self.check_mrl.isChecked())
        self.check_calc_erl.setChecked(self.check_erl.isChecked())
        self.check_calc_orl.setChecked(self.check_orl.isChecked())
        self.check_calc_crl.setChecked(self.check_crl.isChecked())
        self.radio_calc_hard.setChecked(self.radio_hard.isChecked())
        self.radio_calc_soft.setChecked(self.radio_soft.isChecked())
        self.radio_calc_both.setChecked(self.radio_both.isChecked())

        if self.check_calc_trl.isChecked():
            params.append('T')
        if self.check_calc_mrl.isChecked():
            params.append('M')
        if self.check_calc_erl.isChecked():
            params.append('E')
        if self.check_calc_orl.isChecked():
            params.append('O')
        if self.check_calc_crl.isChecked():
            params.append('C')
        if not self.radio_calc_hard.isChecked():
            rad.append('H')
        if not self.radio_calc_soft.isChecked():
            rad.append('S')
        if not self.radio_calc_both.isChecked():
            rad.append('B')

        print('Тип -', rad)
        print('Параметры -', params)
        data = pd.read_excel('Tasks.xlsx', index_col='Тип')
        data.drop(rad, inplace=True)
        for el in params:
            task = self.check_params(data, el)
            tasks_list.append(task)
        self.create_row(tasks_list)

        # df = data.loc[(data['Тип'].isin(rad)) & (data['Параметр'].isin(params))]
        # print(df)

    def check_params(self, df, param):
        row_parent = ''
        tasks = []
        for i, j in df.iterrows():
            if j[1] == param:
                if isinstance(j[2], str) and j[2] != '':
                    row_parent = j[2]
                tasks.append(j[3])
        params = [row_parent, tasks]
        return params

    def create_row(self, tasks):
        for i in range(len(tasks)):
            row_parent = tasks[i][0]
            row_children = tasks[i][1]
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            self.treeWidget.topLevelItem(i).setText(0, row_parent)
            self.treeWidget.expandAll()
            for j in range(len(row_children)):
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setCheckState(0, QtCore.Qt.Unchecked)
                self.treeWidget.topLevelItem(i).child(j).setText(0, row_children[j])

    def calculate(self):
        self.tabWidget.setCurrentIndex(0)
        self.frame_results.setEnabled(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('rjd.png'))
    window.show()
    sys.exit(app.exec_())
