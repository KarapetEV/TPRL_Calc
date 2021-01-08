# -*- coding: utf-8 -*-

#  Copyright 2020 Aleksey Karapyshev, Evgeniy Karapyshev ©
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

import sys, os
import login, register, check_db
import calc_gui
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QToolTip
import pandas as pd
from chart import Chart
from PyQt5.QtCore import pyqtSignal, QSize


style = os.path.join(os.path.dirname(__file__), 'style.css')

class HighlightDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self._filters = []
        self._wordwrap = False
        self.doc = QtGui.QTextDocument(self)


    def paint(self, painter, option, index):
        painter.save()
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)
        if self._wordwrap:
            self.doc.setTextWidth(options.rect.width())
        options.text = ""
        style = QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)

        if self._wordwrap:
            painter.translate(options.rect.left(), options.rect.top())
            clip = QtCore.QRectF(QtCore.QPointF(), QtCore.QSizeF(options.rect.size()))
            self.doc.drawContents(painter, clip)
        else:
            textRect = style.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, options, None)
            if index.column() != 0:
                textRect.adjust(5, 0, 0, 0)
            margin = (option.rect.height() - options.fontMetrics.height()) // 2
            textRect.setTop(textRect.top() + margin)
            painter.translate(textRect.topLeft())
            painter.setClipRect(textRect.translated(-textRect.topLeft()))
            self.doc.documentLayout().draw(painter)

        painter.restore()
        s = QtCore.QSize(self.doc.idealWidth(), self.doc.size().height())
        index.model().setData(index, s, QtCore.Qt.SizeHintRole)

    def filters(self):
        return self._filters

    def setWordWrap(self, on):
        self._wordwrap = on
        mode = QtGui.QTextOption.WordWrap if on else QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere

        textOption = QtGui.QTextOption(self.doc.defaultTextOption())
        textOption.setWrapMode(mode)
        self.doc.setDefaultTextOption(textOption)
        self.parent().viewport().update()

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


class HelpDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(HelpDialog, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''
                           background-color: #fce6e6;
                           border-radius: 5px;
                           border: 2px solid red;
                           ''')
        self.setWindowTitle('Информация о программе')
        x = self.parent().x() + int(self.parent().width() / 2) - 250
        y = self.parent().y() + int(self.parent().height() / 2) - 150
        self.setGeometry(x, y, 500, 300)
        self.help_text = QtWidgets.QTextEdit()
        self.help_text.setStyleSheet('background-color: #f3f3f3;')
        self.help_text.setPlainText('Инструкция!\nДля расчета уровня зрелости инновационного проекта/технологии к '
                                    'внедрению в ОАО «РЖД» необходимо выбрать параметры оценки, по которым производится '
                                    'расчет и нажать кнопку «Установить параметры». В открывшемся поле необходимо '
                                    'отметить те задачи, которые были выполнены в полном объеме на каждом уровне. '
                                    'Результат рассчитывается нажатием кнопки «Расчитать» и представлен в отдельной '
                                    'вкладке «Результаты». Уровень зрелости результата проекта считается достигнутым, '
                                    'если все задачи, относящиеся к различным унифицированным параметрам, отмечены. '
                                    'Общая оценка зрелости проекта принимается равным минимальному достигнутому уровню '
                                    'зрелости по отдельному выбранному параметру.')
        self.help_text.setReadOnly(True)
        self.help_text.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.btn_ok = QtWidgets.QPushButton('OK')
        self.btn_ok.setStyleSheet('background-color: #f24437;')
        self.form = QtWidgets.QFormLayout()
        self.form.setSpacing(20)
        self.form.addRow(self.help_text)
        self.form.addRow(self.btn_ok)
        self.btn_ok.setFixedSize(70, 30)
        self.setLayout(self.form)
        self.btn_ok.clicked.connect(self.close)


class Login(QtWidgets.QDialog, login.Ui_Login):
    enter_data = pyqtSignal(str)

    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.comboBox_users.addItems(check_db.create_user_list())
        self.comboBox_users.currentIndexChanged.connect(self.reset_passw)
        self.btn_choose_user.clicked.connect(self.choose_user)
        self.btn_new_user.clicked.connect(self.register)

    def choose_user(self):
        user = self.comboBox_users.currentText()
        password = self.lineEdit_password.text()
        if check_db.login(user, password):
            self.enter_data.emit(user)
            self.close()
            self.main = Window(user)
            self.main.show()
        else:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Неверный пароль!')
            self.reset_passw()


    def register(self):
        self.close()
        self.register = Register()
        self.register.show()

    def reset_passw(self):
        self.lineEdit_password.setText("")


class Register(QtWidgets.QDialog, register.Ui_Register):
    mysignal = pyqtSignal(str)

    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.btn_register.clicked.connect(self.register)
        self.mysignal.connect(self.signal_handler)

    def register(self):
        user = []
        if self.lineEdit_login_create.text():
            name = self.lineEdit_login_create.text()
            user.append(name)
        if self.lineEdit_password_create.text() == self.lineEdit_password_confirm.text():
            password = self.lineEdit_password_create.text()
            user.append(password)
        else:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Пароль не подтвержден!')
            self.lineEdit_password_create.setText("")
            self.lineEdit_password_confirm.setText("")
        check_db.register(user, self.mysignal)
        self.close()
        self.login = Login()
        self.login.show()

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Ошибка', value)

# class ProjectDialog(QtWidgets.QDialog):
#     enter_data = pyqtSignal(str, str)
#
#     def __init__(self, parent=None):
#
#         super(ProjectDialog, self).__init__(parent)
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setStyleSheet('''
#                            border-radius: 5px;
#                            border: 1px solid red;
#                            ''')
#         self.setWindowTitle('Ввод данных')
#         # desktop = QtWidgets.QApplication.desktop()
#         # x = int(desktop.width()/2) - 150
#         # y = int(desktop.height()/2) - 80
#         x = self.parent().x() + int(self.parent().width() / 2) - 175
#         y = self.parent().y() + int(self.parent().height() / 2) - 50
#         self.setGeometry(x, y, 350, 100)
#         self.line_project_num = QtWidgets.QLineEdit()
#         self.line_project_num.setStyleSheet('''
#                                             border: 1px solid red;
#                                             font-size: 14px;
#                                             ''')
#         self.line_project_num.setMaximumWidth(300)
#         self.line_project_num.setPlaceholderText('Введите номер проекта...')
#         self.line_expert = QtWidgets.QLineEdit()
#         self.line_expert.setStyleSheet('''
#                                        border: 1px solid red;
#                                        font-size: 14px;
#                                        ''')
#         self.line_expert.setMaximumWidth(300)
#         self.line_expert.setPlaceholderText('Введите ФИО эксперта...')
#         self.btn_ok = QtWidgets.QPushButton('OK')
#         self.btn_cancel = QtWidgets.QPushButton('Отмена')
#         self.hbox = QtWidgets.QHBoxLayout()
#         self.hbox.addWidget(self.btn_ok)
#         self.hbox.addWidget(self.btn_cancel)
#         self.form = QtWidgets.QFormLayout()
#         self.form.setSpacing(20)
#         self.form.addRow("&Номер проекта:", self.line_project_num)
#         self.form.addRow("&ФИО эксперта:", self.line_expert)
#         self.form.addRow(self.hbox)
#         self.form.labelForField(self.line_project_num).setStyleSheet('''
#                                                                      border: none;
#                                                                      font-size: 14px;
#                                                                      font-weight: bold;
#                                                                      ''')
#         self.form.labelForField(self.line_expert).setStyleSheet('''
#                                                                 border: none;
#                                                                 font-size: 14px;
#                                                                 font-weight: bold;
#                                                                 ''')
#         self.setLayout(self.form)
#         self.btn_ok.clicked.connect(self.send_data)
#         self.btn_cancel.clicked.connect(self.close)
#
#
#     def send_data(self):
#         if not self.line_project_num.text() or not self.line_expert.text():
#             pass
#         else:
#             self.enter_data.emit(self.line_project_num.text(), self.line_expert.text())
#             self.close()


class Window(QtWidgets.QWidget, calc_gui.Ui_AppWindow):
    parameters = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.tabWidget.setTabEnabled(1, False)
        self.btn_set_params.clicked.connect(self.set_params)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        # self.btn_calculate.clicked.connect(self.create_dialog)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_reset_tasks.clicked.connect(self.reset_tasks)
        self.save_graph_btn.clicked.connect(self.save_chart)
        self.btn_manual.clicked.connect(self.show_help)
        # self.btn_save.clicked.connect(self.save_results)
        self.params = []
        self.project_num = ''
        self.expert_name = user
        self.rad = []
        self.tprl_min = 0
        # self._delegate = HighlightDelegate(self.table_tprl_results)
        # self.table_tprl_results.setItemDelegate(self._delegate)

    # def create_dialog(self):
    #     self.login = Login()
    #     self.login.enter_data[str].connect(self.calculate)

    # def change_ugt_level(self):
    #     labels_ugt = {
    #         self.label_ugt0: [0, 90],
    #         self.label_ugt1: [1, 114],
    #         self.label_ugt2: [2, 142],
    #         self.label_ugt3: [3, 169],
    #         self.label_ugt4: [4, 193],
    #         self.label_ugt5: [5, 221],
    #         self.label_ugt6: [6, 248],
    #         self.label_ugt7: [7, 274],
    #         self.label_ugt8: [8, 300],
    #         self.label_ugt9: [9, 328],
    #     }
    #     result_style = ('''
    #                     background-color: #e21a1a;
    #                     font-family: MS Shell Dlg;
    #                     color: #ffffff;
    #                     font-size: 30px;
    #                     ''')
    #     self.default_labels(labels_ugt)
    #     size = self.ugtSlider.value()
    #     for k, v in labels_ugt.items():
    #         if v[0] == size:
    #             # print(k.font().toString())
    #             x = k.x() - 10
    #             y = k.y() - 5
    #             k.setGeometry(QtCore.QRect(x, y, 33, 30))
    #             k.setStyleSheet(result_style)
    #             k.setEnabled(True)
    #         else:
    #             k.setStyleSheet('''
    #                             background-color: #f3f3f3;
    #                             font-family: MS Shell Dlg;
    #                             color: #e21a1a;
    #                             font-size: 18px;
    #                             ''')
    #             k.setEnabled(False)

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
                pars = level.child(j)
                task_count = pars.childCount()
                for gamma in range(task_count):
                    task = pars.child(gamma)
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
        QToolTip.setFont(QtGui.QFont('Calibri', 9))

        data = pd.read_excel('Test_Tasks.xlsx', sheet_name=self.rad[0])
        val = self.make_level_dict(data, self.params)

        item_color = ''

        for i, key in enumerate(val.items()):
            textEdit_0 = AdjusttableTextEdit()  # key[1][1] - комментарий к key[1][0]
            textEdit_0.setText(key[1][0])
            textEdit_0.setReadOnly(True)
            font_0 = QtGui.QFont()
            font_0.setBold(True)
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget, [f'Уровень {key[0]}', key[1][0]])
            self.treeWidget.setItemWidget(item_0, 1, textEdit_0)
            x = '<nobr>' + key[1][1][:80] + '</nobr>' + key[1][1][80:]

            item_0.setToolTip(1, x)
            textEdit_0.td_size_sig.connect(lambda size: item_0.setSizeHint(1, size))
            item_0.setFont(0, font_0)
            self.treeWidget.expandAll()

            for j, v in enumerate(key[1][2].items()):
                textEdit_1 = AdjusttableTextEdit()
                textEdit_1.setText(v[1][0])
                textEdit_1.setReadOnly(True)
                item_1 = QtWidgets.QTreeWidgetItem(item_0, [v[0], ""])
                self.treeWidget.setItemWidget(item_1, 1, textEdit_1)
                textEdit_1.td_size_sig.connect(lambda size: item_1.setSizeHint(1, size))
                self.treeWidget.expandAll()
                for item in v[1][1:]:
                    textEdit_2 = AdjusttableTextEdit()  # item[1] - комментарий к item[0]
                    textEdit_2.setText(item[0])
                    textEdit_2.setReadOnly(True)
                    item_2 = QtWidgets.QTreeWidgetItem(item_1, ["", ""])
                    item_2.setCheckState(1, QtCore.Qt.Unchecked)
                    item_2.setFlags(QtCore.Qt.ItemIsUserCheckable)
                    item_2.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.treeWidget.setItemWidget(item_2, 1, textEdit_2)
                    y = '<nobr>' + item[1][:80] + '</nobr>' + item[1][80:]
                    item_2.setToolTip(1, y)
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

    def make_params_dict(self, df, x, params):
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
                dict_levels[x] = [df['Level_Name'][row], df['Level_Comments'][row],
                                  self.make_params_dict(df, x, params)]
        return dict_levels

    def create_table_rows(self, text_levels):
        # table = QtWidgets.QTableWidget(self.frame_tprl_results)
        # table.setObjectName('table')

        self.table_tprl_results.setRowCount(len(text_levels))
        self.table_tprl_results.setColumnCount(2)
        self.table_tprl_results.setColumnWidth(0, 50)
        self.table_tprl_results.setColumnWidth(1, 700)
        self.table_tprl_results.setStyleSheet('''font-size: 15px;
                                                        ''')

        for key, values in text_levels.items():
            if key == 'TPRL':
                self.table_tprl_results.setSpan(0, 0, 1, 2)
                self.table_tprl_results.setItem(0, 0, QtWidgets.QTableWidgetItem(values))

        text_levels.pop('TPRL')

        for i, key in enumerate(text_levels.items()):
            self.table_tprl_results.setItem(i+1, 0, QtWidgets.QTableWidgetItem(key[0]))
            self.table_tprl_results.setItem(i+1, 1, QtWidgets.QTableWidgetItem(key[1]))
        # self._delegate.setWordWrap(True)
        self.table_tprl_results.setShowGrid(False)
        self.table_tprl_results.resizeRowsToContents()
        self.table_tprl_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_tprl_results.setEnabled(False)

    #
    # def create_text_rows(self, text_levels):
    #     self.text_other.setText("")
    #     for key, values in text_levels.items():
    #         if key == 'TPRL':
    #             self.text_tprl.setText(values)
    #     text_levels.pop('TPRL')
    #
    #     count_rows = 1
    #     for k, v in text_levels.items():
    #         self.text_other.append(f'{v}')
    #         self.text_other.append('-' * 112)
    #         count_rows += 1

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
        # text_dict = {'TPRL': str(self.ugtSlider.value())}
        text_dict = {'TPRL': str(self.tprl_min)}
        text_dict.update(self.d3)
        text_levels = self.make_text_dict(op_data, text_dict)
        # self.create_text_rows(text_levels)
        self.create_table_rows(text_levels)

    def calculate(self, name):
        # self.label_project_num.setText(num)
        # self.project_num = num
        self.label_expert_name.setText(self.expert_name)
        # self.expert_name = name
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
            for child in range(childs):
                kids = self.treeWidget.topLevelItem(level).child(child).childCount()
                p = self.treeWidget.topLevelItem(level).child(child).text(0)
                for kid in range(kids):
                    kid_item = self.treeWidget.topLevelItem(level).child(child).child(kid)
                    # ch_item = self.treeWidget.topLevelItem(level).child(child)

                    if p not in d2:
                        l2 = []
                        if kid_item.checkState(1) == QtCore.Qt.Checked:
                            l2.append(1)
                        else:
                            l2.append(0)
                        d2[p] = l2
                    else:
                        if kid_item.checkState(1) == QtCore.Qt.Checked:
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
        self.chart = Chart(self.d3, self.lay)
        self.save_graph_btn.setEnabled(True)
        self.make_text()

    def save_chart(self):
        self.chart.save_chart(self.project_num)
        QtWidgets.QMessageBox.about(self, 'Сохранение файла',
                                    f'График успешно сохранен в файле "{self.project_num}_chart.png"!')
        self.save_graph_btn.setEnabled(False)

    def show_results(self, res):
        summa = 0
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
            summa += float(v_res)


        self.tprl_average = float(summa/len(res.values()))
        self.tprl_min = int(self.tprl_average)
        self.label_tprl_average_result.setText(str(self.tprl_average))
        self.label_tprl_min_result.setText(str(self.tprl_min))
        # if int(itog) == 0:
        #     self.ugtSlider.setValue(1)
        #     self.ugtSlider.setValue(0)
        # else:
        #     self.ugtSlider.setValue(int(itog))

    def show_help(self):
        self.help_dialog = HelpDialog(self)
        self.help_dialog.show()

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
    window = Login()  # Создаем экземпляр класса
    window.setWindowTitle('TPRL Calculator')
    window.setWindowIcon(QtGui.QIcon('.\img\\rzd.png'))
    window.show()
    sys.exit(app.exec_())
