import sys, os
import app_gui
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import pandas as pd
from chart import create_chart

style = os.path.join(os.path.dirname(__file__), 'style.css')


class Window(QtWidgets.QWidget, app_gui.Ui_AppWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.tabWidget.setTabEnabled(1, False)
        self.btn_set_params.clicked.connect(self.set_params)
        self.ugtSlider.valueChanged.connect(self.change_ugt_level)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_reset_tasks.clicked.connect(self.reset_tasks)
        self.params = []
        self.rad = []

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
            if v == size:
                print(k.font().toString())
                k.setStyleSheet('''
                                background-color: #e21a1a;
                                font-family: MS Shell Dlg;
                                color: #ffffff;
                                font-size: 24px;
                                ''')
                k.setEnabled(True)
            else:
                k.setStyleSheet('''
                                background-color: #f3f3f3;
                                font-family: MS Shell Dlg;
                                color: #e21a1a;
                                font-size: 18px;
                                ''')
                k.setEnabled(False)

    def reset_params(self):
        self.check_calc_trl.setChecked(False)
        self.check_calc_mrl.setChecked(False)
        self.check_calc_erl.setChecked(False)
        self.check_calc_orl.setChecked(False)
        self.check_calc_crl.setChecked(False)
        self.radio_calc_hard.setChecked(False)
        self.radio_calc_soft.setChecked(False)
        self.radio_calc_both.setChecked(False)
        self.treeWidget.clear()
        self.params = []
        self.rad = []

    def reset_tasks(self):
        levels_count = self.treeWidget.topLevelItemCount()
        for i in range(levels_count):
            level = self.treeWidget.topLevelItem(i)
            childs_count = level.childCount()
            for j in range(childs_count):
                task = level.child(j)
                task.setCheckState(1, QtCore.Qt.Unchecked)

    def set_params(self):
        self.reset_params()
        self.get_params()
        if len(self.params) == 0:
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Не выбраны параметры оценки!')
        else:
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setCurrentIndex(1)
            self.frame_calc_params.setEnabled(False)
            self.create_rows()

    def get_params(self):
        self.check_calc_trl.setChecked(self.check_trl.isChecked())
        self.check_calc_mrl.setChecked(self.check_mrl.isChecked())
        self.check_calc_erl.setChecked(self.check_erl.isChecked())
        self.check_calc_orl.setChecked(self.check_orl.isChecked())
        self.check_calc_crl.setChecked(self.check_crl.isChecked())
        self.radio_calc_hard.setChecked(self.radio_hard.isChecked())
        self.radio_calc_soft.setChecked(self.radio_soft.isChecked())
        self.radio_calc_both.setChecked(self.radio_both.isChecked())

        if self.check_calc_trl.isChecked():
            self.params.append('TRL')
        if self.check_calc_mrl.isChecked():
            self.params.append('MRL')
        if self.check_calc_erl.isChecked():
            self.params.append('ERL')
        if self.check_calc_orl.isChecked():
            self.params.append('ORL')
        if self.check_calc_crl.isChecked():
            self.params.append('CRL')
        if not self.radio_calc_hard.isChecked():
            self.rad.append('H')
        if not self.radio_calc_soft.isChecked():
            self.rad.append('S')
        if not self.radio_calc_both.isChecked():
            self.rad.append('B')

    def create_rows(self):

        data = pd.read_excel('Tasks1.xlsx', index_col='Тип')
        df = data.drop(self.rad)
        val = self.make_level_dict(df, self.params)

        item_color = ''

        for i, key in enumerate(val.items()):
            font = QtGui.QFont()
            font.setBold(True)
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setFont(0, font)
            self.treeWidget.topLevelItem(i).setText(0, 'Уровень {}'.format(key[0]))
            self.treeWidget.expandAll()
            count = 1
            for j, v in enumerate(key[1].items()):

                for idx in range(len(v[1])):
                    item_1 = QtWidgets.QTreeWidgetItem(item_0, [v[0], v[1][idx]])
                    item_1.setCheckState(1, QtCore.Qt.Unchecked)
                    item_1.setFlags(QtCore.Qt.ItemIsUserCheckable)
                    item_1.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.treeWidget.topLevelItem(i).child(count).setText(0, v[0])
                    # self.treeWidget.topLevelItem(i).child(count).setText(1, v[1][idx])

                    if count % 2 == 0:
                        item_color = '#c2c2c2'
                    else:
                        item_color = '#f5f5f5'
                    item_1.setBackground(0, QtGui.QColor(item_color))
                    item_1.setBackground(1, QtGui.QColor(item_color))
                count += 1

    def make_params_dict(self, df, params):
        d_2 = {}
        for row in range(df['Параметр'].shape[0]):
            for p in params:
                if df['Параметр'][row] == p:
                    if df['Параметр'][row] not in d_2:
                        d_2[df['Параметр'][row]] = [df['Задача'][row]]
                    else:
                        d_2[df['Параметр'][row]].append(df['Задача'][row])
        return d_2

    def make_level_dict(self, df, params):
        d_1 = {}
        for level in df['Уровень'].unique():
            if level not in d_1:
                x = [str(level)]
                d = df.loc[df['Уровень'].isin(x)]
                d_1[x[0]] = self.make_params_dict(d, params)
        return d_1

    def calculate(self):
        d1 = {}
        self.d3 = {}
        levels = self.treeWidget.topLevelItemCount()
        for level in range(levels):
            l1 = []
            childs = self.treeWidget.topLevelItem(level).childCount()
            topLevelItemText = self.treeWidget.topLevelItem(level).text(0)
            d2 = {}
            for kid in range(childs):
                p = self.treeWidget.topLevelItem(level).child(kid).text(0)
                ch_item = self.treeWidget.topLevelItem(level).child(kid)
                if p not in d2:
                    l2 = []
                    if ch_item.checkState(1) == QtCore.Qt.Checked:
                        l2.append(1)
                    else:
                        l2.append(0)
                    d2[p] = l2
                else:
                    if ch_item.checkState(1) == QtCore.Qt.Checked:
                        d2[p].append(1)
                    else:
                        d2[p].append(0)

            for k, v in d2.items():
                v = round(sum(v) / len(v), 1)
                d2[k] = v
                if k not in self.d3:
                    self.d3[k] = [v]
                else:
                    self.d3[k].append(v)
            if level not in d1:
                d1[topLevelItemText] = d2
        print(self.d3)
        for key, values in self.d3.items():
            summary = 0
            for iter_value in range(len(values)):
                if values[iter_value] == 1:
                    summary += 1
                elif 0 < values[iter_value] < 1:
                    summary += values[iter_value]
                    self.d3[key] = str(summary)
                    break
                else:
                    self.d3[key] = str(summary)
                    break
        print('До обработки', self.d3)
        x = float(max(self.d3.values()))
        y = float(min(self.d3.values()))
        if x - y > 2:
            for iter_k, iter_v in self.d3.items():
                iter_v = float(iter_v)
                if iter_v == x:
                    self.d3[iter_k] = str(round(iter_v - 1, 1))
        print('После обработки', self.d3)
        self.tabWidget.setCurrentIndex(0)
        self.frame_results.setEnabled(True)
        self.show_results(self.d3)
        create_chart(self.d3, self.frame_graph)

    def show_results(self, res):
        summa = 0

        for k_res, v_res in res.items():
            summa += float(v_res)
            if k_res == 'TRL':
                self.label_trl_result.setText(v_res)
            elif k_res == 'MRL':
                self.label_mrl_result.setText(v_res)
            elif k_res == 'ERL':
                self.label_erl_result.setText(v_res)
            elif k_res == 'ORL':
                self.label_orl_result.setText(v_res)
            elif k_res == 'CRL':
                self.label_crl_result.setText(v_res)
        average_f = float(summa / 5)
        average_i = int(average_f)
        self.ugtSlider.setValue(average_i)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def onItemClicked(self, item):
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
        else:
            if item.checkState(1) == QtCore.Qt.Unchecked:
                item.setCheckState(1, QtCore.Qt.Checked)
            else:
                item.setCheckState(1, QtCore.Qt.Unchecked)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()                   # Создаем экземпляр класса
    window.setWindowTitle('TRL Calculator')
    window.setWindowIcon(QtGui.QIcon('.\img\\rzd.png'))
    window.show()
    sys.exit(app.exec_())
