# -*- coding: utf-8 -*-

#  Copyright 2020 Aleksey Karapyshev, Evgeniy Karapyshev ©
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

import sys, os, datetime
import login, register, check_db
import calc_gui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QToolTip
import numpy as np
import pandas as pd
from chart import Chart
from PyQt5.QtCore import pyqtSignal, QSize
from splash import Splash

style = os.path.join(os.path.dirname(__file__), 'style.css')

class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        self.setGeometry((QtCore.QRect(0, 0, 815, 380)))
        self.setColumnWidth(0, 150)
        self.headerItem().setText(0, 'Параметр')
        self.headerItem().setText(1, 'Задачи')


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
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint)
        self.setStyleSheet(open(style).read())
        self.setWindowTitle('Информация о программе')
        x = self.parent().x() + int(self.parent().width() / 2) - 200
        y = self.parent().y() + int(self.parent().height() / 2) - 125
        self.setGeometry(x, y, 400, 250)
        self.help_text = QtWidgets.QTextEdit(self)
        self.help_text.setGeometry(10, 10, 380, 180)
        self.help_text.setStyleSheet('background-color: #f3f3f3;')
        self.help_text.setAlignment(QtCore.Qt.AlignHCenter)
        self.help_text.insertPlainText('Инструкция!\n')
        self.help_text.setAlignment(QtCore.Qt.AlignLeft)
        self.help_text.insertPlainText('Для расчета уровня зрелости инновационного проекта/технологии к '
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
        self.btn_ok = QtWidgets.QPushButton(self)
        # self.btn_ok.setStyleSheet(open(style).read())
        self.btn_ok.setGeometry(150, 205, 100, 30)
        self.btn_ok.setText("OK")
        self.btn_ok.clicked.connect(self.close)


class Login(QtWidgets.QDialog, login.Ui_Login):
    switch_register = pyqtSignal()
    switch_mainwindow = pyqtSignal(str)

    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.comboBox_users.addItems(check_db.create_user_list())
        self.comboBox_users.setCurrentIndex(0)
        self.comboBox_users.currentIndexChanged.connect(self.reset_passw)
        self.btn_choose_user.clicked.connect(self.choose_user)
        self.btn_new_user.clicked.connect(self.register)

    def choose_user(self):
        user = self.comboBox_users.currentText()
        if not user:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Пользователь не выбран!')
        else:
            password = self.lineEdit_password.text()
            if check_db.login(user, password):
                self.switch_mainwindow.emit(user)
            else:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Неверный пароль!')
                self.reset_passw()

    def register(self):
        self.switch_register.emit()

    def reset_passw(self):
        self.lineEdit_password.setText("")


class Register(QtWidgets.QDialog, register.Ui_Register):
    mysignal = pyqtSignal(str)
    switch_login = pyqtSignal()

    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.btn_register.clicked.connect(self.register)
        self.btn_back.clicked.connect(self.get_back)
        self.mysignal.connect(self.signal_handler)

    def register(self):
        user = []
        chars = ':\/*?<>"|'
        if self.lineEdit_login_create.text():
            for ch in chars:
                if ch in self.lineEdit_login_create.text():
                    QtWidgets.QMessageBox.about(self, 'Ошибка', 'Имя не должно содержать символы :\/*?<>"| !')
                    self.lineEdit_login_create.setText("")
                    self.lineEdit_password_create.setText("")
                    self.lineEdit_password_confirm.setText("")
                    return
            name = self.lineEdit_login_create.text()
            user.append(name)
            if self.lineEdit_password_create.text() == self.lineEdit_password_confirm.text():
                password = self.lineEdit_password_create.text()
                user.append(password)
                check_db.register(user, self.mysignal)
            else:
                QtWidgets.QMessageBox.about(self, 'Ошибка', 'Пароль не подтвержден!')
                self.lineEdit_password_create.setText("")
                self.lineEdit_password_confirm.setText("")
        else:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Не введен логин!')
            self.lineEdit_password_create.setText("")
            self.lineEdit_password_confirm.setText("")
        self.switch_login.emit()

    def get_back(self):
        self.switch_login.emit()

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Ошибка', value)


# class ProjectDialog(QtWidgets.QDialog):
#     enter_data = pyqtSignal(str)
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
#         self.btn_ok = QtWidgets.QPushButton('OK')
#         self.btn_cancel = QtWidgets.QPushButton('Отмена')
#         self.hbox = QtWidgets.QHBoxLayout()
#         self.hbox.addWidget(self.btn_ok)
#         self.hbox.addWidget(self.btn_cancel)
#         self.form = QtWidgets.QFormLayout()
#         self.form.setSpacing(20)
#         self.form.addRow("&Номер проекта:", self.line_project_num)
#         self.form.addRow(self.hbox)
#         self.form.labelForField(self.line_project_num).setStyleSheet('''
#                                                                      border: none;
#                                                                      font-size: 14px;
#                                                                      font-weight: bold;
#                                                                      ''')
#         self.setLayout(self.form)
#         self.btn_ok.clicked.connect(self.send_data)
#         self.btn_cancel.clicked.connect(self.close)
#
#     def send_data(self):
#         if not self.line_project_num.text():
#             pass
#         else:
#             self.enter_data.emit(self.line_project_num.text())
#             self.close()


class Window(QtWidgets.QWidget, calc_gui.Ui_AppWindow):
    switch_login = pyqtSignal()

    parameters = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setStyleSheet(open(style).read())
        self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setTabEnabled(4, False)
        # self.treeWidget.itemClicked.connect(self.onItemClicked)

        self.expert_name = user
        self.params = []
        self.project_num = ''
        self.rad = []
        self.tprl_min = 0
        self.project_state = ''
        self.label_user_name.setText(user)
        self.label_user_name1.setText(user)
        self.label_user_name2.setText(user)
        self.newproject_data = tuple()
        self.saveproject_data = tuple()

        self.btn_set_params.clicked.connect(self.set_params)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_reset_tasks.clicked.connect(self.reset_tasks)
        self.btn_manual.clicked.connect(self.show_help)
        self.btn_save_results.clicked.connect(self.save_results)
        self.btn_change_user.clicked.connect(self.change_user)
        self.btn_change_user1.clicked.connect(self.change_user)
        self.btn_change_user2.clicked.connect(self.change_user)
        self.btn_load_project.clicked.connect(self.load_project_data)
        self.btn_load_project2.clicked.connect(self.load_project_data)
        self.btn_new_project.clicked.connect(self.create_dialog)
        self.tabWidget.currentChanged.connect(self.show_user_projects)
        self.save_data = pd.DataFrame(
            columns=['Level', 'Pars_Name', 'Task', 'Task_Comments', 'Original_Task', 'State', 'Parameter'])

    @QtCore.pyqtSlot(int)
    def show_user_projects(self, index):
        if index == 1:
            drafts = check_db.load_project(self.expert_name, 'черновик')
            self.create_table(self.projects_table, drafts)
        elif index == 2:
            complete = check_db.load_project(self.expert_name, 'итог')
            self.create_table(self.projects_table2, complete)
        else:
            pass

    def create_table(self, tab_widget, data):
        tab_widget.setSortingEnabled(False)
        tab_widget.setRowCount(len(data))
        for row, form in enumerate(data):
            tab_widget.setRowHeight(0, 20)
            form = ((str(row + 1)),) + form
            for column, cell in enumerate(form):
                if column == 0:
                    item = QtWidgets.QTableWidgetItem(str(row + 1))
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
                    tab_widget.setColumnWidth(column, 50)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    tab_widget.setItem(row, column, item)
                else:
                    item = QtWidgets.QTableWidgetItem(str(cell))
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
                    tab_widget.setItem(row, column, item)
        tab_widget.resizeColumnsToContents()
        tab_widget.setColumnWidth(3, 200)
        tab_widget.setSortingEnabled(True)

    def change_user(self):
        self.switch_login.emit()
        self.expert_name = ''
        self.label_user_name.setText("")
        self.label_user_name1.setText("")
        self.label_user_name2.setText("")
        self.projects_table.clear()
        self.projects_table2.clear()

    def load_project_data(self):
        self.set_param_check(self.parameters, False)
        self.reset_params()
        data = [self.expert_name]
        table = None
        if self.tabWidget.currentIndex() == 1:
            table = self.projects_table
        elif self.tabWidget.currentIndex() == 2:
            table = self.projects_table2
        row = table.currentRow()
        num = table.item(row, 1).text()
        data.append(num)
        date = table.item(row, 6).text()
        data.append(date)
        value = check_db.get_project(data)
        self.project_state = value[0]
        self.path = value[1]
        self.params = value[2].split(' ')
        self.project_num = num
        self.tabWidget.setTabEnabled(3, True)
        self.tabWidget.setCurrentIndex(3)
        self.btn_calculate.setEnabled(True)
        self.btn_reset_tasks.setEnabled(True)
        self.num_calcTab.setText(self.project_num)
        self.user_calcTab.setText(self.expert_name)
        self.set_param_check(self.params, True)
        self.create_rows()

    def start_project(self, num):
        self.project_num = num
        self.set_param_check(self.parameters, False)
        self.reset_params()
        self.project_state = ''
        temp = []
        for item in self.tab_new_project.children():
            if isinstance(item, QtWidgets.QLineEdit):
                temp.append(item.text())
                item.setText("")
        self.newproject_data = tuple(temp)
        self.tabWidget.setTabEnabled(3, True)
        self.tabWidget.setCurrentIndex(3)
        self.num_calcTab.setText(self.project_num)
        self.user_calcTab.setText(self.expert_name)

    def create_dialog(self):
        if self.expert_name == '':
            QtWidgets.QMessageBox.about(self, "Внимание!", "Не выбран пользователь!")
            self.switch_login.emit()
        else:
            self.check_enterdata()

    def check_enterdata(self):
        full_info = True
        for item in self.tab_new_project.children():
            if isinstance(item, QtWidgets.QLineEdit) and item.text() == '':
                full_info = False
        if not full_info:
            QtWidgets.QMessageBox.about(self, "Внимание!", "Не все поля заполнены!")
        else:
            project_num = self.enter_project_num.text()
            self.start_project(project_num)

    def set_param_check(self, params, bool):
        for el in self.group_params.children():
            for param in self.params:
                if param.lower() in el.objectName().title().lower():
                    el.setChecked(bool)

    def reset_params(self):
        self.save_data = pd.DataFrame(
            columns=['Level', 'Pars_Name', 'Task', 'Task_Comments', 'Original_Task', 'State', 'Parameter'])
        self.param_tabs.clear()
        self.params = []
        self.rad = []

    def confirm_msg(self, text):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setWindowTitle("Подтверждение")
        messageBox.setIcon(QtWidgets.QMessageBox.Question)
        messageBox.setText(f"Вы уверены, что хотите {text}?")
        buttonYes = messageBox.addButton("Да", QtWidgets.QMessageBox.YesRole)
        buttonNo = messageBox.addButton("Нет", QtWidgets.QMessageBox.NoRole)
        messageBox.setDefaultButton(buttonYes)
        messageBox.exec_()

        if messageBox.clickedButton() == buttonYes:
            return True
        elif messageBox.clickedButton() == buttonNo:
            return False

    def reset_tasks(self):
        text = "сбросить все отметки"
        if self.confirm_msg(text):
            tab_count = self.param_tabs.count()
            for i in range(tab_count):
                self.param_tabs.setCurrentIndex(i)
                tree = self.param_tabs.currentWidget()
                root = tree.invisibleRootItem()
                for level_num in range(root.childCount()):
                    level = root.child(level_num)
                    for j in range(level.childCount()):
                        child = level.child(j)
                        el = tree.itemWidget(child, 0)
                        if isinstance(el, QtWidgets.QComboBox):
                            el.setCurrentText('Нет')
            self.param_tabs.setCurrentIndex(0)

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
        # if self.radio_hard.isChecked():
        #     self.rad.append('H')
        # if self.radio_soft.isChecked():
        #     self.rad.append('S')
        # if self.radio_both.isChecked():
        #     self.rad.append('B')

    def create_rows(self):
        QToolTip.setFont(QtGui.QFont('Calibri', 9))

        for param in self.params:
            if self.project_state in ['черновик', 'итог']:
                self.data = pd.read_excel(self.path, sheet_name=param)
            else:
                self.data = pd.read_excel('Param_Tasks.xlsx', sheet_name=param)
            self.data['Parameter'] = param
            val = self.make_level_dict(self.data)

            self.tw = TreeWidget()
            self.param_tabs.addTab(self.tw, param)
            self.param_tabs.setCurrentIndex(self.params.index(param))
            self.param_tabs.setTabEnabled(self.params.index(param), True)

            for key, value in val.items():
                textEdit_0 = AdjusttableTextEdit()  # key[1][1] - комментарий к key[1][0]
                textEdit_0.setText(value[0])
                textEdit_0.setReadOnly(True)
                font_0 = QtGui.QFont()
                font_0.setBold(True)
                self.item_0 = QtWidgets.QTreeWidgetItem(self.tw, [f'Уровень {key}', ""])
                self.tw.setItemWidget(self.item_0, 1, textEdit_0)
                # x = '<nobr>' + key[1][1][:80] + '</nobr>' + key[1][1][80:]
                #
                # item_0.setToolTip(1, x)
                textEdit_0.td_size_sig.connect(lambda size: self.item_0.setSizeHint(1, size))
                self.item_0.setFont(0, font_0)
                self.tw.expandAll()

                for v in value[1:]:
                    self.combo_task = QtWidgets.QComboBox()
                    self.combo_task.addItems(['Да', 'Нет', 'Не применимо'])
                    self.combo_task.setFixedSize(110, 20)
                    textEdit_1 = AdjusttableTextEdit()
                    textEdit_1.setText(v[0])
                    textEdit_1.setReadOnly(True)
                    self.item_1 = QtWidgets.QTreeWidgetItem(self.item_0, ["", ""])
                    if v[2] == 0:
                        self.combo_task.setCurrentText('Нет')
                    elif v[2] == 1:
                        self.combo_task.setCurrentText('Да')
                    else:
                        self.combo_task.setCurrentText('Не применимо')

                    self.tw.setItemWidget(self.item_1, 0, self.combo_task)
                    self.tw.setItemWidget(self.item_1, 1, textEdit_1)
                    textEdit_1.td_size_sig.connect(lambda size: self.item_1.setSizeHint(1, size))
                    text_style = '''background-color: #fce6e6;
                                    border: 0;
                                    font-size: 13px;
                                    color: #000;
                                    '''
                    textEdit_0.setStyleSheet(text_style)
                    textEdit_1.setStyleSheet(text_style)

                    self.item_1.setBackground(0, QtGui.QColor('#f5f5f5'))
            self.save_data = self.save_data.append(self.data)
        self.param_tabs.setCurrentIndex(0)

    # def make_params_dict(self, df, x, params):
    #     dict_params = {}
    #     for row in range(df['Level'].shape[0]):
    #         if df['Level'][row] == x:
    #             for p in params:
    #                 if df['Parameter'][row] == p:
    #                     if df['Parameter'][row] not in dict_params:
    #                         dict_params[df['Parameter'][row]] = [df['Pars_Name'][row], [df['Task'][row],
    #                                                                                     df['Task_Comments'][row],
    #                                                                                     df['State'][row]]]
    #                     else:
    #                         dict_params[df['Parameter'][row]].append(
    #                             [df['Task'][row], df['Task_Comments'][row], df['State'][row]])
    #     return dict_params

    def make_level_dict(self, df):
        dict_levels = {}
        for row in range(df['Level'].shape[0]):
            if df['Level'][row] not in dict_levels:
                dict_levels[df['Level'][row]] = [df['Pars_Name'][row],
                                                 [df['Task'][row],
                                                  df['Task_Comments'][row],
                                                  df['State'][row]]]
            else:
                dict_levels[df['Level'][row]].append([df['Task'][row],
                                                      df['Task_Comments'][row],
                                                      df['State'][row]])
        return dict_levels

    def create_table_rows(self, text_levels):

        self.table_tprl_results.setRowCount(len(text_levels) - 1)
        self.table_tprl_results.setColumnCount(2)
        self.table_tprl_results.setColumnWidth(0, 50)
        self.table_tprl_results.setColumnWidth(1, 700)
        self.table_tprl_results.setStyleSheet('''font-size: 14px;
                                                        ''')

        for key, values in text_levels.items():
            if key == 'TPRL':
                self.label_main_tprl.setText(f'{values}')


        text_levels.pop('TPRL')
        for i, key in enumerate(text_levels.items()):
            label1 = QtWidgets.QLabel(key[0])
            label1.setStyleSheet("border-bottom: 1px solid;")
            label1.setMaximumHeight(50)
            label2 = QtWidgets.QLabel(key[1])
            label2.setStyleSheet("border-bottom: 1px solid;")
            label2.setMaximumHeight(50)
            label2.setWordWrap(True)
            self.table_tprl_results.setCellWidget(i, 0, label1)
            self.table_tprl_results.setCellWidget(i, 1, label2)
            # self.table_tprl_results.setItem(i, 0, QtWidgets.QTableWidgetItem(key[0]))
            # self.table_tprl_results.item(i, 0).setFlags(QtCore.Qt.ItemIsEditable)
            # self.table_tprl_results.setItem(i, 1, QtWidgets.QTableWidgetItem(key[1]))
            # self.table_tprl_results.item(i, 1).setFlags(QtCore.Qt.ItemIsEditable)
        # self._delegate.setWordWrap(True)
        self.table_tprl_results.setShowGrid(False)
        self.table_tprl_results.resizeRowsToContents()
        self.table_tprl_results.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.table_tprl_results.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_tprl_results.setEnabled(True)

    def make_text_dict(self, op_data, diction):
        new_text_dict = {}
        for key, value in diction.items():
            for rank in range(op_data['Уровень'].shape[0]):
                if (key == 'TPRL') & (value == '0'):
                    new_text_dict['TPRL'] = 'Уровень зрелости инновационного проекта/технологии  = 0'
                elif (key == 'TPRL') & (value == '--'):
                    new_text_dict['TPRL'] = 'Уровень зрелости инновационного проекта/технологии не рассчитан, т.к. не были выбраны все параметры'
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

    def calculate(self):
        # self.save_data = self.data.copy()
        # self.save_data = self.save_data.loc[self.save_data['Parameter'].isin(self.params)]
        self.save_data.drop(['State'], axis='columns', inplace=True)
        self.label_project_num.setText(self.project_num)
        self.label_expert_name.setText(self.expert_name)
        self.tabWidget.setTabEnabled(4, True)
        self.tabWidget.setCurrentIndex(4)
        self.check_draft.setEnabled(True)
        self.check_draft.setChecked(False)
        self.btn_save_results.setEnabled(True)
        d1 = {}
        d2 = {}
        self.d3 = {}
        new_state = []
        l2 = []
        for param in self.params:
            self.param_tabs.setCurrentIndex(self.params.index(param))
            tree = self.param_tabs.currentWidget()
            root = tree.invisibleRootItem()
            levels = root.childCount()
            # l2 = []
            for level_num in range(levels):
                level = root.child(level_num)
                # print(param, level)
                #     d2 = {}
                l1 = []
                for kid in range(level.childCount()):
                    child = level.child(kid)
                    el = tree.itemWidget(child, 0)
                    if isinstance(el, QtWidgets.QComboBox):
                        combo_text = el.currentText()
                        if combo_text == 'Да':
                            l1.append(1)
                            new_state.append(1)
                        elif combo_text == 'Нет':
                            l1.append(0)
                            new_state.append(0)
                        else:
                            l1.append(-1)
                            new_state.append(-1)
                if param not in d1:
                    l2 = []
                    l2.append(l1)
                    d1[param] = l2
                else:
                    d1[param].append(l1)

            # print(d1)

            for key, values in d1.items():
                first_list = []
                for value in values:
                    new_list = []
                    for v in range(len(value)):
                        if value[v] == 1:
                            new_list.append(1)
                        if value[v] == 0:
                            new_list.append(0)
                    first_list.append(new_list)
                d2[key] = first_list
        self.save_data['State'] = new_state
        for new_key, new_values in d2.items():
            l_n = []
            for new_value in new_values:
                new_value = round(sum(new_value) / len(new_value), 1)
                l_n.append(new_value)
            d2[new_key] = l_n

        for d2_keys, d2_values in d2.items():
            summary = 0
            for d2_value in range(len(d2_values)):
                if d2_values[d2_value] == 1:
                    summary += 1
                elif 0 < d2_values[d2_value] < 1:
                    summary += d2_values[d2_value]
                    break
                else:
                    break
            self.d3[d2_keys] = str(summary)
        for par in Window.parameters:
            if par not in self.d3.keys():
                self.d3[par] = '0'
        for iter_k, iter_v in self.d3.items():
            iter_v = float(iter_v)
        if float(max(self.d3.values())) - float(min(self.d3.values())) > 2:
            x = float(max(self.d3.values()))
        else:
            x = -1
        for d3_k, d3_v in self.d3.items():
            if float(d3_v) == x:
                self.d3[d3_k] = str(float(d3_v) - 1)
            else:
                self.d3[d3_k] = d3_v
        self.frame_results.setEnabled(True)
        self.show_results(self.d3)
        self.chart = Chart(self.d3, self.lay)
        self.make_text()
        # d1 = {}
        # self.d3 = {}
        # l2 = []
        # levels = self.treeWidget.topLevelItemCount()
        # l1 = []
        # for level in range(levels):
        #     childs = self.treeWidget.topLevelItem(level).childCount()
        #     topLevelItemText = self.treeWidget.topLevelItem(level).text(0)
        #     d2 = {}
        #     for child in range(childs):
        #         kids = self.treeWidget.topLevelItem(level).child(child).childCount()
        #         p = self.treeWidget.topLevelItem(level).child(child).text(0)
        #         for kid in range(kids):
        #             kid_item = self.treeWidget.topLevelItem(level).child(child).child(kid)
        #             # ch_item = self.treeWidget.topLevelItem(level).child(child)
        #             # -----------------Добавляем в новый State значение (0/1)
        #             if kid_item.checkState(1) == QtCore.Qt.Checked:
        #                 l1.append(1)
        #             else:
        #                 l1.append(0)
        #             # ------------Продолжаем формировать словарь---------------
        #             if p not in d2:
        #                 l2 = []
        #                 if kid_item.checkState(1) == QtCore.Qt.Checked:
        #                     l2.append(1)
        #                 else:
        #                     l2.append(0)
        #                 d2[p] = l2
        #             else:
        #                 if kid_item.checkState(1) == QtCore.Qt.Checked:
        #                     d2[p].append(1)
        #                 else:
        #                     d2[p].append(0)
        #
        #     for k, v in d2.items():
        #         v = round(sum(v) / len(v), 1)
        #         d2[k] = v
        #         if k not in self.d3:
        #             self.d3[k] = [v]
        #         else:
        #             self.d3[k].append(v)
        #     if level not in d1:
        #         d1[topLevelItemText] = d2
        # self.save_data['State'] = l1
        # for key, values in self.d3.items():
        #     summary = 0
        #     for iter_value in range(len(values)):
        #         if values[iter_value] == 1:
        #             summary += 1
        #         elif 0 < values[iter_value] < 1:
        #             summary += values[iter_value]
        #             # self.d3[key] = str(summary)
        #             break
        #         else:
        #             # self.d3[key] = str(summary)
        #             break
        #     self.d3[key] = str(summary)
        # for param in Window.parameters:
        #     if param not in self.d3.keys():
        #         self.d3[param] = '0'
        # for iter_k, iter_v in self.d3.items():
        #     iter_v = float(iter_v)
        #     # self.d3[iter_k] = iter_v
        # # print('После обработки', self.d3)
        # self.frame_results.setEnabled(True)
        # self.show_results(self.d3)
        # self.chart = Chart(self.d3, self.lay)
        # # self.save_graph_btn.setEnabled(True)
        # self.make_text()

    def save_results(self):
        # ---------------Формируем dataframe с результатами------------------------
        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y %H:%M")
        file_date = now.strftime("%d.%m.%Y")
        if self.check_draft.isChecked():
            self.project_state = 'черновик'
        else:
            self.project_state = 'итог'
        chars = ':\/*?<>"|'
        saved_file_name = self.project_num
        for ch in chars:
            if ch in saved_file_name:
                saved_file_name = saved_file_name.replace(ch, '_')
        if '\\' in saved_file_name:
            saved_file_name = saved_file_name.replace('\\', '_')
        project_dir = f'{saved_file_name}_{file_date}'
        new_file_name = f'{saved_file_name}_{file_date}.xlsx'
        total = [[self.expert_name, self.project_num, date, self.label_tprl_min_result.text(),
                  self.label_tprl_average_result.text(), self.label_trl_result.text(),
                  self.label_mrl_result.text(), self.label_erl_result.text(),
                  self.label_orl_result.text(), self.label_crl_result.text(), self.project_state]]
        features = np.array(total)
        columns = ['Expert', 'Project Number', 'Date', 'TPRLmin', 'TPRLaverage', 'TRL', 'MRL', 'ERL', 'ORL', 'CRL',
                   'Статус']
        frame = pd.DataFrame(data=features, columns=columns)
        # ---------------Записываем данные в файл----------------------------------
        file_name = 'Results.xlsx'
        if os.path.isfile(file_name):
            old_frame = pd.read_excel('Results.xlsx')
            old_frame = old_frame.append(frame, ignore_index=True)
            old_frame.to_excel('Results.xlsx', index=False)
        else:
            file = open('Results.xlsx', 'w')
            frame.to_excel('Results.xlsx', index=False)
            file.close()
        # ---------------Записываем данные в файл_2--------------------------------------------
        if not os.path.isdir("Projects"):
            os.mkdir("Projects")
        if not os.path.isdir(f"Projects/{self.expert_name}"):
            os.mkdir(f"Projects/{self.expert_name}")
        if self.project_state == 'черновик':
            if not os.path.isdir(f"Projects/{self.expert_name}/Черновики"):
                os.mkdir(f"Projects/{self.expert_name}/Черновики")
            os.mkdir(f"Projects/{self.expert_name}/Черновики/{project_dir}")
            self.path = f"Projects/{self.expert_name}/Черновики/{project_dir}/{new_file_name}"
            # new_file = open(self.path, 'w')
            writer = pd.ExcelWriter(self.path)
            for param in self.params:
                new_save_data = self.save_data.loc[self.save_data['Parameter'].isin([param])]
                new_save_data.drop(['Parameter'], axis='columns', inplace=True)
                # new_save_data.to_excel(self.path, index=False, sheet_name=param)
                new_save_data.to_excel(writer, sheet_name=param)
                writer.save()
            writer.close()
            # new_file.close()
        else:
            if not os.path.isdir(f"Projects/{self.expert_name}/Завершенные"):
                os.mkdir(f"Projects/{self.expert_name}/Завершенные")
            os.mkdir(f"Projects/{self.expert_name}/Завершенные/{project_dir}")
            self.path = f"Projects/{self.expert_name}/Завершенные/{project_dir}/{new_file_name}"
            full_dir = f"Projects/{self.expert_name}/Завершенные/{project_dir}"
            # new_file = open(self.path, 'w')
            writer = pd.ExcelWriter(self.path)
            for param in self.params:
                new_save_data = self.save_data.loc[self.save_data['Parameter'].isin([param])]
                new_save_data.drop(['Parameter'], axis='columns', inplace=True)
                # new_save_data.to_excel(self.path, index=False, sheet_name=param)
                new_save_data.to_excel(writer, sheet_name=param)
                writer.save()
            writer.close()
            # new_file.close()
            self.chart.save_chart(full_dir, project_dir)

        # сохранение проекта в БД
        params = ' '.join(self.params)
        self.saveproject_data = (date, self.project_state, self.path, params)
        data = self.newproject_data + self.saveproject_data
        check_db.save_project(self.expert_name, data)

        QtWidgets.QMessageBox.about(self, 'Сохранение результатов', 'Результаты успешно сохранены')
        self.btn_save_results.setEnabled(False)
        self.check_draft.setEnabled(False)

    def show_results(self, res):
        res_list = []
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
            res_list.append(float(v_res))
        if len(self.params) < 5:
            self.tprl_average = '--'
            self.tprl_min = '--'
            self.label_tprl_average_result.setText(self.tprl_average)
            self.label_tprl_min_result.setText(self.tprl_min)
        else:
            self.tprl_average = float(sum(res_list) / len(res_list))
            self.tprl_min = int(self.tprl_average)

            self.label_tprl_average_result.setText(str(self.tprl_average))
            self.label_tprl_min_result.setText(str(self.tprl_min))

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

    def closeEvent(self, event):
        text = "закрыть программу"
        if self.confirm_msg(text):
            event.accept()
        else:
            event.ignore()


class Controller:

    def __init__(self):
        self.login = None
        self.register = None
        self.window = None
        self.splashscreen = None

    def show_splash(self):
        self.splashscreen = Splash()
        self.splashscreen.show()
        app.processEvents()
        self.show_login_page()

    def show_login_page(self):
        self.login = Login()
        self.login.switch_register.connect(self.show_register_page)
        self.login.switch_mainwindow[str].connect(self.show_mainwindow)
        if self.register:
            self.register.close()
        self.login.show()
        if self.splashscreen:
            self.splashscreen.finish(self.login)

    def show_register_page(self):
        self.register = Register()
        self.register.switch_login.connect(self.show_login_page)
        self.login.close()
        self.register.show()

    def show_mainwindow(self, user):
        self.window = Window(user)
        self.window.switch_login.connect(self.show_login_page)
        self.login.close()
        self.window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()  # Создаем экземпляр класса
    controller.show_splash()
    sys.exit(app.exec_())
