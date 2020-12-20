import sys, os
import calcv2_gui
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import pandas as pd
from chart import create_chart
from PyQt5.QtCore import pyqtSignal, QSize

style = os.path.join(os.path.dirname(__file__), 'style.css')
class AdjusttableTextEdit(QtWidgets.QTextEdit):
    td_size_sig = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super(AdjusttableTextEdit, self).__init__(parent)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.resizeTextEdit)
        self.document().documentLayout().documentSizeChanged.connect(self.resizeTextEdit)

    def resizeTextEdit(self):
        docheight = int(self.document().size().height())
        margin = int(self.document().documentMargin())
        self.setMinimumHeight(docheight + margin)
        self.setMaximumHeight(docheight + margin)

        return
    def resizeEvent(self, e):
        super(AdjusttableTextEdit, self).resizeEvent(e)
        self.td_size_sig.emit(QSize(self.sizeHint().width(), self.maximumHeight()))
        return


class ProjectDialog(QtWidgets.QDialog):
    enter_data = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(ProjectDialog, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''
                           border-radius: 5px;
                           border: 1px solid red;
                           ''')
        self.setWindowTitle('Ввод данных')
        # desktop = QtWidgets.QApplication.desktop()
        # x = int(desktop.width()/2) - 150
        # y = int(desktop.height()/2) - 80
        x = self.parent().x() + int(self.parent().width() / 2) - 175
        y = self.parent().y() + int(self.parent().height() / 2) - 50
        self.setGeometry(x, y, 350, 100)
        self.line_project_num = QtWidgets.QLineEdit()
        self.line_project_num.setStyleSheet('''
                                            border: 1px solid red;
                                            font-size: 14px;
                                            ''')
        self.line_project_num.setMaximumWidth(300)
        self.line_project_num.setPlaceholderText('Введите номер проекта...')
        self.line_expert = QtWidgets.QLineEdit()
        self.line_expert.setStyleSheet('''
                                       border: 1px solid red;
                                       font-size: 14px;
                                       ''')
        self.line_expert.setMaximumWidth(300)
        self.line_expert.setPlaceholderText('Введите ФИО эксперта...')
        self.btn_ok = QtWidgets.QPushButton('OK')
        self.btn_cancel = QtWidgets.QPushButton('Отмена')
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.btn_ok)
        self.hbox.addWidget(self.btn_cancel)
        self.form = QtWidgets.QFormLayout()
        self.form.setSpacing(20)
        self.form.addRow("&Номер проекта:", self.line_project_num)
        self.form.addRow("&ФИО эксперта:", self.line_expert)
        self.form.addRow(self.hbox)
        self.form.labelForField(self.line_project_num).setStyleSheet('''
                                                                     border: none;
                                                                     font-size: 14px;
                                                                     font-weight: bold;
                                                                     ''')
        self.form.labelForField(self.line_expert).setStyleSheet('''
                                                                border: none;
                                                                font-size: 14px;
                                                                font-weight: bold;
                                                                ''')
        self.setLayout(self.form)
        self.btn_ok.clicked.connect(self.send_data)
        self.btn_cancel.clicked.connect(self.close)

    def send_data(self):
        if not self.line_project_num.text() or not self.line_expert.text():
            pass
        else:
            self.enter_data.emit(self.line_project_num.text(), self.line_expert.text())
            self.close()


class Window(QtWidgets.QWidget, calcv2_gui.Ui_AppWindow):

    parameters = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        # self.project_dialog = ProjectDialog(self)
        self.tabWidget.setTabEnabled(1, False)
        self.btn_set_params.clicked.connect(self.set_params)
        self.ugtSlider.valueChanged.connect(self.change_ugt_level)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.btn_calculate.clicked.connect(self.create_dialog)
        self.btn_reset_tasks.clicked.connect(self.reset_tasks)
        self.params = []
        # self.project_dialog.enter_data[str, str].connect(self.calculate)
        self.project_num = ''
        self.expert_name = ''
        self.rad = []

    def create_dialog(self):
        self.project_dialog = ProjectDialog(self)
        self.project_dialog.show()
        self.project_dialog.enter_data[str, str].connect(self.calculate)

    def change_ugt_level(self):
        labels_ugt = {
            self.label_ugt0: [0, 90],
            self.label_ugt1: [1, 114],
            self.label_ugt2: [2, 142],
            self.label_ugt3: [3, 169],
            self.label_ugt4: [4, 193],
            self.label_ugt5: [5, 221],
            self.label_ugt6: [6, 248],
            self.label_ugt7: [7, 274],
            self.label_ugt8: [8, 300],
            self.label_ugt9: [9, 328],
        }
        result_style = ('''
                        background-color: #e21a1a;
                        font-family: MS Shell Dlg;
                        color: #ffffff;
                        font-size: 30px;
                        ''')
        self.default_labels(labels_ugt)
        size = self.ugtSlider.value()
        for k, v in labels_ugt.items():
            if v[0] == size:
                # print(k.font().toString())
                x = k.x() - 10
                y = k.y() - 5
                k.setGeometry(QtCore.QRect(x, y, 33, 30))
                k.setStyleSheet(result_style)
                k.setEnabled(True)
            else:
                k.setStyleSheet('''
                                background-color: #f3f3f3;
                                font-family: MS Shell Dlg;
                                color: #e21a1a;
                                font-size: 18px;
                                ''')
                k.setEnabled(False)

    def default_labels(self, labels):
        for k, v in labels.items():
            k.setGeometry(v[1], 120, 15, 23)

    def reset_params(self):
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
            self.create_rows()
            self.btn_calculate.setEnabled(True)
            self.btn_reset_tasks.setEnabled(True)

    def get_params(self):

        if self.check_trl.isChecked():
            self.params.append('TRL')
        if self.check_mrl.isChecked():
            self.params.append('MRL')
        if self.check_erl.isChecked():
            self.params.append('ERL')
        if self.check_orl.isChecked():
            self.params.append('ORL')
        if self.check_crl.isChecked():
            self.params.append('CRL')
        if self.radio_hard.isChecked():
            self.rad.append('H')
        if self.radio_soft.isChecked():
            self.rad.append('S')
        if self.radio_both.isChecked():
            self.rad.append('B')

    def create_rows(self):

        data = pd.read_excel('Test_Tasks.xlsx', sheet_name=self.rad[0])
        val = self.make_level_dict(data, self.params)

        item_color = ''

        for i, key in enumerate(val.items()):
            textEdit_0 = AdjusttableTextEdit()
            textEdit_0.setText(key[1][0])
            textEdit_0.setReadOnly(True)
            font_0 = QtGui.QFont()
            font_0.setBold(True)
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget, [f'Уровень {key[0]}', key[1][0]])
            self.treeWidget.setItemWidget(item_0, 1, textEdit_0)
            textEdit_0.td_size_sig.connect(lambda size: item_0.setSizeHint(1, size))
            item_0.setFont(0, font_0)
            # self.treeWidget.topLevelItem(i).setText(0, 'Уровень {}'.format(key[0]))
            # self.treeWidget.topLevelItem(i).setText(1, key[1][0])
            self.treeWidget.expandAll()

            for j, v in enumerate(key[1][2].items()):
                textEdit_1 = AdjusttableTextEdit()
                textEdit_1.setText(v[1][0])
                textEdit_1.setReadOnly(True)
                item_1 = QtWidgets.QTreeWidgetItem(item_0, [v[0], ""])
                self.treeWidget.setItemWidget(item_1, 1, textEdit_1)
                textEdit_1.td_size_sig.connect(lambda size: item_1.setSizeHint(1, size))
                # self.treeWidget.setText(0, v[0])
                # self.treeWidget.setText(1, v[1][0])
                self.treeWidget.expandAll()
                for item in v[1][1:]:
                    textEdit_2 = AdjusttableTextEdit()
                    textEdit_2.setText(item[0])
                    textEdit_2.setReadOnly(True)
                    item_2 = QtWidgets.QTreeWidgetItem(item_1, ["", ""])
                    item_2.setCheckState(1, QtCore.Qt.Unchecked)
                    item_2.setFlags(QtCore.Qt.ItemIsUserCheckable)
                    item_2.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.treeWidget.setItemWidget(item_2, 1, textEdit_2)
                    textEdit_2.td_size_sig.connect(lambda size: item_2.setSizeHint(1, size))

                    textEdit_0.setStyleSheet('''background-color: #fce6e6;
                                                border: 0;
                                                font-size: 13px;
                                                color: #000;
                                                ''')
                    textEdit_1.setStyleSheet('''background-color: #f5f5f5;
                                                border: 0;
                                                font-size: 13px;
                                                color: #000;
                                                ''')
                    textEdit_2.setStyleSheet('''background-color: #fce6e6;
                                                border: 0;
                                                font-size: 13px;
                                                color: #000;
                                                ''')
                    item_1.setBackground(0, QtGui.QColor('#f5f5f5'))
                    # item_2.setBackground(0, QtGui.QColor(item_color))
                    # item_2.setBackground(1, QtGui.QColor(item_color))


    def make_params_dict(self, df, x,  params):
        dict_params = {}
        for row in range(df['Level'].shape[0]):
            if df['Level'][row] == x:
                for p in params:
                    if df['Parameter'][row] == p:
                        if df['Parameter'][row] not in dict_params:
                            dict_params[df['Parameter'][row]] = [df['Pars_Name'][row], [df['Task'][row],
                                                                                            df['Task_Comments'][row]]]
                        else:
                            dict_params[df['Parameter'][row]].append([df['Task'][row], df['Task_Comments'][row]])
        return dict_params

    def make_level_dict(self, df, params):
        dict_levels = {}
        for row in range(df['Level'].shape[0]):
            if df['Level'][row] not in dict_levels:
                x = df['Level'][row]
                dict_levels[x] = [df['Level_Name'][row], df['Level_Comments'][row], self.make_params_dict(df, x, params)]
        return dict_levels

    def create_text_rows(self, text_levels):
        self.text_other.setText("")
        for key, values in text_levels.items():
            if key == 'TPRL':
                self.text_tprl.setText(values)
        text_levels.pop('TPRL')

        count_rows = 1
        for k, v in text_levels.items():
            # if count_rows % 2 == 0:
            #     self.text_other.setTextBackgroundColor(QtGui.QColor('#c2c2c2'))
            # else:
            #     self.text_other.setTextBackgroundColor(QtGui.QColor('#f3f3f3'))
            self.text_other.append(f'{v}')
            self.text_other.append('-'*115)
            count_rows += 1

    def make_text_dict(self, op_data, diction):
        new_text_dict = {}
        for key, value in diction.items():
            for rank in range(op_data['Уровень'].shape[0]):
                if (key == 'TPRL') & (value == '0'):
                    new_text_dict['TPRL'] = 'Уровень зрелости инновационного проекта/технологии  = 0'
                elif op_data['Уровень'][rank] == int(float(value)):
                    new_text_dict[key] = op_data[key][rank]
        return new_text_dict

    def make_text(self):
        op_data = pd.read_excel('Levels.xlsx')
        text_dict = {'TPRL': str(self.ugtSlider.value())}
        text_dict.update(self.d3)
        text_levels = self.make_text_dict(op_data, text_dict)
        self.create_text_rows(text_levels)

    def calculate(self, num, name):
        self.label_project_num.setText(num)
        self.label_expert_name.setText(name)
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentIndex(1)
        d1 = {}
        self.d3 = {}
        l2 = []
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
            # print(d2)
            for k, v in d2.items():
                v = round(sum(v) / len(v), 1)
                d2[k] = v
                if k not in self.d3:
                    self.d3[k] = [v]
                else:
                    self.d3[k].append(v)
            if level not in d1:
                d1[topLevelItemText] = d2
        # print(self.d3)
        for key, values in self.d3.items():
            summary = 0
            for iter_value in range(len(values)):
                if values[iter_value] == 1:
                    summary += 1
                elif 0 < values[iter_value] < 1:
                    summary += values[iter_value]
                    # self.d3[key] = str(summary)
                    break
                else:
                    # self.d3[key] = str(summary)
                    break
            self.d3[key] = str(summary)
        for param in Window.parameters:
            if param not in self.d3.keys():
                self.d3[param] = '0'
        # print('До обработки', self.d3)
        # x = float(max(self.d3.values()))
        # y = float(min(self.d3.values()))
        # if x - y > 2:
        #     for iter_k, iter_v in self.d3.items():
        #         iter_v = float(iter_v)
        #         if iter_v == x:
        #             self.d3[iter_k] = str(round(iter_v - 1, 1))
        for iter_k, iter_v in self.d3.items():
            iter_v = float(iter_v)
            # self.d3[iter_k] = iter_v
        # print('После обработки', self.d3)
        self.frame_results.setEnabled(True)
        self.show_results(self.d3)
        create_chart(self.d3, self.lay)
        self.make_text()

    def show_results(self, res):

        for k_res, v_res in res.items():
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
        itog = float(min(res.values()))
        if int(itog) == 0:
            self.ugtSlider.setValue(1)
            self.ugtSlider.setValue(0)
        else:
            self.ugtSlider.setValue(int(itog))


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
