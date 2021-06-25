# -*- coding: utf-8 -*-

# © Copyright 2021 Aleksey Karapyshev, Evgeniy Karapyshev
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

# This file is part of TPRL Calculator.
#
#     TPRL Calculator is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

from decimal import Decimal
import sys
import os
import datetime
import login
import register
import check_db
import calcv2_gui
import numpy as np
import pandas as pd
from chart import Chart
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QDialog, \
    QLabel, QPushButton, QMessageBox, QTabWidget, QTableWidgetItem, QLineEdit, QComboBox, QFrame, QHeaderView
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRect
from splash import Splash
from report_ugt import ReportUgt
from report_risks import ReportRisks

style = os.path.join(os.path.dirname(__file__), 'style.css')


class comboCompanies(QComboBox):                                # комбобоксы в таблице рисков
    combo_signal = pyqtSignal()

    def __init__(self, parent):
        super(comboCompanies, self).__init__(parent)
        self.setStyleSheet("font-size: 12px;")
        self.addItems(['1', '2', '3', '4', '5'])
        self.setCurrentText('1')
        self.currentIndexChanged.connect(self.combo_signal.emit)


class TreeWidget(QTreeWidget):                                  # задачи по параметрам
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        self.setGeometry((QRect(0, 0, 815, 380)))
        self.setColumnWidth(0, 150)
        self.headerItem().setText(0, 'Параметр')
        self.headerItem().setText(1, 'Задачи')
        self.setStyleSheet("QHeaderView::section {background-color: #82898E; font-size: 14px; "
                           "font-weight: bold; color: #ffffff;}")
        self.itemClicked.connect(self.onItemClicked)

    @pyqtSlot(QTreeWidgetItem)
    def onItemClicked(self, item):
        if item.isExpanded():
            item.setExpanded(False)
        else:
            item.setExpanded(True)


class HelpDialog(QDialog):

    def __init__(self, parent=None):
        # Создание окна "Помощь"
        super(HelpDialog, self).__init__(parent)
        self.setStyleSheet(open(style).read())
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )
        self.setWindowTitle('Информация о программе')
        self.btn_ok = QPushButton(self)
        self.btn_ok.setGeometry(185, 330, 100, 30)
        self.btn_ok.setText("OK")
        self.btn_ok.clicked.connect(self.close)

        # Указание координат для формирования окна - в центре
        x = self.parent().x() + int(self.parent().width() / 2) - 200
        y = self.parent().y() + int(self.parent().height() / 2) - 125
        self.setGeometry(x, y, 470, 370)

        # Создание TabWidget для вкладок ("О программе" и "Лицензия")
        self.help_tabs = QTabWidget(self)
        self.help_tabs.setEnabled(True)
        self.help_tabs.setGeometry(QRect(0, 0, 470, 320))
        self.help_tabs.setObjectName("help_tabs")
        self.help_tabs.raise_()

        # Вкладка "О программе"
        self.about_tab = QWidget()
        self.about_tab.setObjectName("about_tab")
        self.help_tabs.addTab(self.about_tab, "О программе")
        self.create_help_tab()

        # Вкладка "Лицензия"
        self.license_tab = QWidget()
        self.license_tab.setObjectName("license_tab")
        self.help_tabs.addTab(self.license_tab, "Лицензия")
        self.create_license_tab()

    def create_help_tab(self):
        self.label_about_title = QLabel(self.about_tab)
        self.label_about_title.setGeometry(QRect(100, 5, 300, 50))
        self.label_about_title.setContentsMargins(0, 0, 0, 0)
        self.label_about_title.setScaledContents(True)
        self.label_about_title.setObjectName("label_about_title")
        self.label_about_title.setPixmap(QPixmap("img/splash_appname.png"))
        self.label_about_title.setAlignment(Qt.AlignCenter)

        help_font = QFont()
        help_font.setPointSize(12)
        help_font.setBold(False)
        help_font.setWeight(35)
        self.help_text = QLabel(self.about_tab)
        self.help_text.setFont(help_font)
        self.help_text.setGeometry(QRect(10, 55, 450, 170))
        self.help_text.setObjectName("help_text")
        self.help_text.setAlignment(Qt.AlignCenter)
        self.help_text.setWordWrap(True)
        self.help_text.setContentsMargins(0, 0, 0, 0)
        self.help_text.setText(
            '<p><small>Программа <strong>"TPRL Calculator"</strong> предназначена для расчёта уровня зрелости '
            'инновационного продукта/технологии, реализующая Методику оценки зрелости инновационного '
            'продукта/технологии к внедрению в ОАО «РЖД» и оценки уровня рисков реализации и финансирования '
            'инновационных проектов в ОАО «РЖД».\n'
            'Все расчеты и результаты, а также оценка рисков формируются в соответствии с представленной '
            'Методикой.</small></p>'
            '<p>© Copyright 2021</p>'
            '<p>\n<small>Алексей Карапышев, Евгений Карапышев<br>'
            'в составе коллектива Дирекции НТП</small></p>'
            '<p>Версия: 1.1</p>')
        self.link = QLabel('<a href="http://fcntp.ru">Посетить сайт Дирекции НТП</a>', self.about_tab)
        self.link.setStyleSheet("font-size: 12px;")
        self.link.setOpenExternalLinks(True)
        self.link.setGeometry(QRect(10, 230, 450, 20))
        self.link.setObjectName("link")
        self.link.setAlignment(Qt.AlignCenter)

        # Кнопка открытия файла методики
        self.btn_methodology = QPushButton(self.about_tab)
        self.btn_methodology.setGeometry(33, 260, 185, 20)
        self.btn_methodology.setObjectName("btn_methodology")
        self.btn_methodology.setText("Методика")
        self.btn_methodology.clicked.connect(self.open_methodology)

        # Кнопка открытия файла руководства пользователя
        self.btn_manual = QPushButton(self.about_tab)
        self.btn_manual.setGeometry(252, 260, 185, 20)
        self.btn_manual.setObjectName("btn_manual")
        self.btn_manual.setText("Руководство пользователя")
        self.btn_manual.clicked.connect(self.open_manual)

    def open_methodology(self):
        # open_path = os.getcwd() + "\\data\\methodology.pdf"
        open_path = os.getcwd() + "/data/methodology.pdf"
        os.startfile(open_path)

    def open_manual(self):
        # open_path = os.getcwd() + "\\data\\manual.pdf"
        open_path = os.getcwd() + "/data/manual.pdf"
        os.startfile(open_path)

    def create_license_tab(self):
        text = ('TPRL Calculator является свободным программным обеспечением: вы можете '
                'распространять и/или изменять его на условиях Стандартной общественной '
                'лицензии GNU в том виде, в каком она была опубликованной Фондом свободного '
                'программного обеспечения (FSF); либо Лицензии версии 3, либо (на Ваше '
                'усмотрение) любой более поздней версии.\n\n'
                'Эта программа распространяется в надежде, что она будет полезной, но БЕЗ КАКИХ '
                'БЫ ТО НИ БЫЛО ГАРАНТИЙНЫХ ОБЯЗАТЕЛЬСТВ; даже без косвенных гарантийных '
                'обязательств, связанных с ПОТРЕБИТЕЛЬСКИМИ СВОЙСТВАМИ и ПРИГОДНОСТЬЮ ДЛЯ '
                'ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Для подробностей смотрите Стандартную Общественную '
                'Лицензию GNU.\n\n'
                'Вы должны были получить копию Стандартной Общественной Лицензии GNU вместе с '
                'этой программой.\nЕсли это не так, см. <https://www.gnu.org/licenses/>.')
        license_font = QFont()
        license_font.setPointSize(10)
        license_font.setBold(False)
        license_font.setWeight(25)
        self.license_text = QLabel(text, self.license_tab)
        self.license_text.setOpenExternalLinks(True)
        self.license_text.setFont(license_font)
        self.license_text.setGeometry(QRect(5, 0, 460, 240))
        self.license_text.setContentsMargins(0, 0, 0, 0)
        self.license_text.setWordWrap(True)
        self.license_text.setObjectName("label_about_title")

        self.btn_license = QPushButton(self.license_tab)
        self.btn_license.setGeometry(160, 260, 150, 20)
        self.btn_license.setObjectName("btn_license")
        self.btn_license.setText("Лицензия GPL")
        self.btn_license.clicked.connect(self.open_license)

    def open_license(self):
        open_path = os.getcwd() + "\\data\\license.pdf"
        os.startfile(open_path)


class Login(QDialog, login.Ui_Login):
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
            QMessageBox.about(self, 'Ошибка', 'Пользователь не выбран!')
        else:
            password = self.lineEdit_password.text()
            if check_db.login(user, password):
                self.switch_mainwindow.emit(user)
            else:
                QMessageBox.about(self, 'Ошибка', 'Неверный пароль!')
                self.reset_passw()

    def register(self):
        self.switch_register.emit()

    def reset_passw(self):
        self.lineEdit_password.setText("")


class Register(QDialog, register.Ui_Register):
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
                    QMessageBox.about(self, 'Ошибка', 'Имя не должно содержать символы :\/*?<>"| !')
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
                QMessageBox.about(self, 'Ошибка', 'Пароль не подтвержден!')
                self.lineEdit_password_create.setText("")
                self.lineEdit_password_confirm.setText("")
        else:
            QMessageBox.about(self, 'Ошибка', 'Не введен логин!')
            self.lineEdit_password_create.setText("")
            self.lineEdit_password_confirm.setText("")
        self.switch_login.emit()

    def get_back(self):
        self.switch_login.emit()

    def signal_handler(self, value):
        QMessageBox.about(self, 'Ошибка', value)


class Window(QWidget, calcv2_gui.Ui_AppWindow):
    switch_login = pyqtSignal()

    parameters = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']

    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setStyleSheet(open(style).read())

        self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setTabEnabled(4, False)
        self.tabWidget.setTabEnabled(5, False)

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
        self.risk_flag = True

        self.btn_set_params.clicked.connect(self.set_params)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_reset_tasks.clicked.connect(self.reset_tasks)
        self.btn_help.clicked.connect(self.show_help)
        self.btn_save_results.clicked.connect(self.save_results)
        self.btn_change_user.clicked.connect(self.change_user)
        self.btn_change_user1.clicked.connect(self.change_user)
        self.btn_change_user2.clicked.connect(self.change_user)
        self.btn_load_project.clicked.connect(self.load_project_data)
        self.btn_remove_project.clicked.connect(self.remove_project)
        self.btn_load_project2.clicked.connect(self.load_project_data)
        self.btn_new_project.clicked.connect(self.create_dialog)
        self.tabWidget.currentChanged.connect(self.show_user_projects)
        self.btn_report_ugt.clicked.connect(self.report_ugt)
        # self.btn_report_risks.clicked.connect(self.report_risks)

        self.save_data = pd.DataFrame(
            columns=['Level', 'Pars_Name', 'Task', 'Task_Comments', 'Original_Task', 'State', 'Parameter'])
        # self.normal_risks = {'Ф1': 33, 'Ф2': 62, 'Ф3': 55, 'Ф4': 30, 'Ф5': 28, 'Ф6': 29,
        #                      'Ф7': 69, 'Ф8': 30, 'Ф9': 22, 'Ф10': 19, 'Ф11': 29, 'Ф12': 30,
        #                      'Ф13': 15, 'Ф14': 5, 'Ф15': 9, 'Ф16': 3, 'Ф17': 13, 'Ф18': 14,
        #                      'Ф19': 223}

    @pyqtSlot(int)
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
        for i in range(len(data)):
            tab_widget.setRowHeight(i, 20)
        for row, form in enumerate(data):
            form = ((str(row + 1)),) + form
            for column, cell in enumerate(form):
                if column == 0:
                    item = QTableWidgetItem(str(row + 1))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled)
                    tab_widget.setColumnWidth(column, 50)
                    item.setTextAlignment(Qt.AlignCenter)
                    tab_widget.setItem(row, column, item)
                else:
                    item = QTableWidgetItem(str(cell))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled)
                    tab_widget.setItem(row, column, item)
        tab_widget.resizeColumnsToContents()
        tab_widget.setColumnWidth(3, 200)
        tab_widget.setSortingEnabled(True)

    def change_user(self):
        self.switch_login.emit()

    def start_project(self, num):
        self.project_num = num
        self.set_param_check(self.parameters, False)
        self.reset_params()
        self.project_state = ''
        temp = []
        for item in self.tab_new_project.children():
            if isinstance(item, QLineEdit):
                temp.append(item.text())
                item.setText("")
        self.newproject_data = tuple(temp)
        self.tabWidget.setTabEnabled(3, True)
        self.tabWidget.setCurrentIndex(3)
        self.num_calcTab.setText(self.project_num)
        self.user_calcTab.setText(self.expert_name)

    def load_project_data(self):
        table = None
        if self.tabWidget.currentIndex() == 1:
            table = self.projects_table
        elif self.tabWidget.currentIndex() == 2:
            table = self.projects_table2
        if len(table.selectedItems()) == 0:
            QMessageBox.about(self, "Внимание!", "Не выбран проект для загрузки!")
        else:
            index = self.tabWidget.currentIndex()
            self.set_param_check(self.parameters, False)
            self.reset_params()
            data = [self.expert_name]
            row = table.currentRow()
            num = table.item(row, 1).text()
            data.append(num)
            date = table.item(row, 6).text()
            data.append(date)
            value = check_db.get_project(data)
            self.newproject_data = (value[3:])
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
            try:
                self.create_rows()
            except FileNotFoundError:
                self.tabWidget.setTabEnabled(index, True)
                self.tabWidget.setCurrentIndex(index)
                if self.confirm_msg("Файлы проекта не найдены! Вы хотите удалить выбранный проект из списка?"):
                    self.delete_from_table(table)

    def remove_project(self):
        table = self.projects_table
        if len(self.projects_table.selectedItems()) == 0:
            QMessageBox.about(self, "Внимание!", "Не выбран проект для удаления!")
        else:
            if self.confirm_msg("Вы уверены, что хотите удалить выбранный проект?"):
                self.delete_from_table(table)

    def delete_from_table(self, table):
        data = [self.expert_name]
        row = table.currentRow()
        num = table.item(row, 1).text()
        data.append(num)
        date = table.item(row, 6).text()
        data.append(date)
        file_path = check_db.remove_project(data)
        index = file_path.rfind('/')
        line = file_path.replace('/', '\\')
        dir_path = f'\\{line[:index]}'
        dir = os.getcwd() + dir_path
        try:
            os.remove(file_path)
            os.rmdir(dir)
        except:
            pass
        self.show_user_projects(self.tabWidget.currentIndex())

    def create_dialog(self):
        if self.expert_name == '':
            QMessageBox.about(self, "Внимание!", "Не выбран пользователь!")
            self.switch_login.emit()
        else:
            self.check_enterdata()

    def check_enterdata(self):
        full_info = True
        for item in self.tab_new_project.children():
            if isinstance(item, QLineEdit) and item.text() == '':
                full_info = False
        if not full_info:
            QMessageBox.about(self, "Внимание!", "Не все поля заполнены!")
        else:
            project_num = self.enter_project_num.text()
            self.start_project(project_num)

    def set_param_check(self, params, bool):
        for el in self.group_params.children():
            for param in params:
                if param.lower() in el.objectName().title().lower():
                    el.setChecked(bool)

    def reset_params(self):
        self.path = 'data/Param_Tasks.xlsx'
        self.save_data = pd.DataFrame(
            columns=['Level', 'Pars_Name', 'Task', 'Task_Comments', 'Original_Task', 'State', 'Parameter'])
        self.param_tabs.clear()
        self.params = []
        self.rad = []

    def confirm_msg(self, text):
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle("Подтверждение")
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setText(text)
        buttonYes = messageBox.addButton("Да", QMessageBox.YesRole)
        buttonNo = messageBox.addButton("Нет", QMessageBox.NoRole)
        messageBox.setDefaultButton(buttonYes)
        messageBox.exec_()

        if messageBox.clickedButton() == buttonYes:
            return True
        elif messageBox.clickedButton() == buttonNo:
            return False

    def reset_tasks(self):
        if self.confirm_msg("Вы уверены, что хотите сбросить все отметки?"):
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
                        if isinstance(el, QComboBox):
                            el.setCurrentText('Нет')
            self.param_tabs.setCurrentIndex(0)

    def set_params(self):
        if self.project_state in ['черновик', 'итог']:
            if self.confirm_msg('Вы уверены, что хотите изменить параметры (текущие отметки будут сброшены)?'):
                self.reset_params()
                self.get_params()
                if len(self.params) == 0:
                    QMessageBox.warning(self, 'Предупреждение', 'Не выбраны параметры оценки!')
                else:
                    self.create_rows()
                    self.btn_calculate.setEnabled(True)
                    self.btn_reset_tasks.setEnabled(True)
        else:
            self.reset_params()
            self.get_params()
            if len(self.params) == 0:
                QMessageBox.warning(self, 'Предупреждение', 'Не выбраны параметры оценки!')
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

    def create_rows(self):

        for param in self.params:
            self.data = pd.read_excel(self.path, sheet_name=param)
            self.data['Parameter'] = param
            val = self.make_level_dict(self.data)

            self.tw = TreeWidget()
            self.param_tabs.addTab(self.tw, param)
            self.param_tabs.setCurrentIndex(self.params.index(param))
            self.param_tabs.setTabEnabled(self.params.index(param), True)

            for key, value in val.items():
                self.item_0 = QTreeWidgetItem(self.tw)
                self.item_0.setBackground(0, QColor("#D3D3D3"))
                self.item_0.setText(0, f'Уровень {key}')
                self.item_0.setBackground(1, QColor("#D3D3D3"))
                text = self.word_wrap(value[0], 90)
                self.item_0.setText(1, text)

                for v in value[1:]:
                    self.combo_task = QComboBox()
                    self.combo_task.setObjectName('combo_task')
                    self.combo_task.addItems(['Да', 'Нет', 'Не применимо'])
                    self.combo_task.adjustSize()
                    self.combo_task.setFixedSize(110, 20)
                    self.item_1 = QTreeWidgetItem(self.item_0, ["", ""])
                    if v[2] == 0:
                        self.combo_task.setCurrentText('Нет')
                    elif v[2] == 1:
                        self.combo_task.setCurrentText('Да')
                    else:
                        self.combo_task.setCurrentText('Не применимо')

                    self.tw.setItemWidget(self.item_1, 0, self.combo_task)
                    text = self.word_wrap(v[0], 90)
                    self.item_1.setText(1, text)
                    self.item_1.setBackground(0, QColor('#fcfcfc'))
                    self.item_1.setBackground(1, QColor('#fcfcfc'))
            self.save_data = self.save_data.append(self.data)
        self.param_tabs.setCurrentIndex(0)

    def word_wrap(self, line, x):
        start = 0
        if len(line) > x:
            while len(line) > (start + x):
                index = line.rfind(' ', start, start + x)
                line = (line[:index]).strip() + "\n" + (line[index:]).strip()
                start = index
        return line

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
        self.table_tprl_results.setStyleSheet('''font-size: 14px;''')

        for key, values in text_levels.items():
            if key == 'TPRL':
                self.label_main_tprl.setText(self.word_wrap(values, 95))

        text_levels.pop('TPRL')
        for i, key in enumerate(text_levels.items()):
            label1 = QLabel(key[0])
            label1.setContentsMargins(5, 5, 5, 5)
            label1.setStyleSheet("border-bottom: 1px solid grey;")
            label_text = self.word_wrap(key[1], 90)
            label2 = QLabel(label_text)
            label2.setContentsMargins(5, 5, 5, 5)
            label2.setStyleSheet("border-bottom: 1px solid grey;")
            self.table_tprl_results.setCellWidget(i, 0, label1)
            self.table_tprl_results.setCellWidget(i, 1, label2)
        self.table_tprl_results.setShowGrid(False)
        self.table_tprl_results.resizeRowsToContents()
        self.table_tprl_results.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_tprl_results.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_tprl_results.setEnabled(True)
        self.table_tprl_results.setFrameStyle(QFrame.NoFrame)

    def make_text_dict(self, op_data, diction):
        new_text_dict = {}
        for key, value in diction.items():
            for rank in range(op_data['Уровень'].shape[0]):
                if (key == 'TPRL') & (value == '0'):
                    new_text_dict['TPRL'] = 'Уровень зрелости инновационного проекта/технологии  = 0'
                elif (key == 'TPRL') & (value == '--'):
                    new_text_dict['TPRL'] = 'Уровень зрелости инновационного проекта/технологии не рассчитан, т.к. ' \
                                            'не были выбраны все параметры'
                elif op_data['Уровень'][rank] == int(float(value)):
                    new_text_dict[key] = op_data[key][rank]
        return new_text_dict

    def make_text(self):
        op_data = pd.read_excel('data/Levels.xlsx')
        text_dict = {'TPRL': str(self.tprl_min)}
        text_dict.update(self.d3)
        text_levels = self.make_text_dict(op_data, text_dict)
        self.create_table_rows(text_levels)

    def calculate(self):
        self.risk_flag = True
        # self.risks_table.setVisible(False)
        self.text_warning = ''
        self.save_data.drop(['State'], axis='columns', inplace=True)
        self.label_project_num.setText(self.project_num)
        self.label_expert_name.setText(self.expert_name)
        self.risks_label_project_num.setText(self.project_num)
        self.risks_label_expert_name.setText(self.expert_name)
        self.tabWidget.setTabEnabled(4, True)
        self.tabWidget.setTabEnabled(5, True)
        self.tabWidget.setCurrentIndex(4)
        self.check_draft.setEnabled(True)
        self.check_draft.setChecked(False)
        self.btn_save_results.setEnabled(True)
        self.d1 = {}
        d2 = {}
        self.d3 = {}
        new_state = []
        l2 = []
        for param in self.params:
            self.param_tabs.setCurrentIndex(self.params.index(param))
            tree = self.param_tabs.currentWidget()
            root = tree.invisibleRootItem()
            levels = root.childCount()
            for level_num in range(levels):
                level = root.child(level_num)
                l1 = []
                for kid in range(level.childCount()):
                    child = level.child(kid)
                    el = tree.itemWidget(child, 0)
                    if isinstance(el, QComboBox):
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
                if param not in self.d1:
                    l2 = []
                    l2.append(l1)
                    self.d1[param] = l2
                else:
                    self.d1[param].append(l1)

            for key, values in self.d1.items():
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
                try:
                    new_value = sum(new_value) / len(new_value)
                    n = Decimal(f'{new_value}')
                    new_value = n.quantize(Decimal('1.0'), rounding='ROUND_HALF_UP')
                except Exception:
                    new_value = 0.0
                l_n.append(new_value)
            d2[new_key] = l_n
        for d2_keys, d2_values in d2.items():
            summary = 0
            for d2_value in range(len(d2_values)):
                if d2_values[d2_value] == 1:
                    if d2_value > 0:
                        if d2_values[d2_value - 1] != 1:
                            self.text_warning = 'Вы не отметили задачи предыдущих уровней.\n' \
                                                'Риски рассчитаны неправильно!!!'
                            self.risk_flag = False
                    summary = d2_value + 1
                elif 0 < d2_values[d2_value] < 1:
                    if summary == d2_value:
                        summary += d2_values[d2_value]
            self.d3[d2_keys] = str(summary)

        # if len(self.params) == 5:  # Оценка рисков
        #     self.risks_table.setVisible(True)
        #     self.count_risks(self.save_data)
        # else:
        #     self.text_warning = 'Комплексная оценка рисков не проводилась, т.к. не все параметры выбраны!'
        #     self.risks_table.setVisible(False)
        #     self.risk_flag = False
        # self.risks_warning_label.setText(self.text_warning)
        # self.btn_report_risks.setEnabled(self.risk_flag)

        self.show_risks()

        for par in Window.parameters:
            if par not in self.d3.keys():
                self.d3[par] = '0'
        for iter_k, iter_v in self.d3.items():
            # iter_v = round(float(iter_v), 1)

            self.d3[iter_k] = str(iter_v)
        self.param_tabs.setCurrentIndex(0)
        self.frame_results.setEnabled(True)
        self.show_results(self.d3)
        if len(self.params) == 5:
            self.chart = Chart(self.d3, self.lay)
        self.make_text()

    def save_results(self):
        # ---------------Формируем dataframe с результатами------------------------
        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y %H:%M")
        file_date = now.strftime("%d.%m.%Y %H-%M")
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
            if not os.path.isdir(f"Projects/{self.expert_name}/Черновики/{saved_file_name}"):
                os.mkdir(f"Projects/{self.expert_name}/Черновики/{saved_file_name}")
            self.path = f"Projects/{self.expert_name}/Черновики/{saved_file_name}/{new_file_name}"
            writer = pd.ExcelWriter(self.path)
            for param in self.params:
                new_save_data = self.save_data.loc[self.save_data['Parameter'].isin([param])]
                new_save_data.drop(['Parameter'], axis='columns', inplace=True)
                new_save_data.to_excel(writer, sheet_name=param, index=False)
                writer.save()
            writer.close()
        else:
            if not os.path.isdir(f"Projects/{self.expert_name}/Завершенные"):
                os.mkdir(f"Projects/{self.expert_name}/Завершенные")
            if not os.path.isdir(f"Projects/{self.expert_name}/Завершенные/{saved_file_name}"):
                os.mkdir(f"Projects/{self.expert_name}/Завершенные/{saved_file_name}")
            self.path = f"Projects/{self.expert_name}/Завершенные/{saved_file_name}/{new_file_name}"
            full_dir = f"Projects/{self.expert_name}/Завершенные/{saved_file_name}"
            writer = pd.ExcelWriter(self.path)
            for param in self.params:
                new_save_data = self.save_data.loc[self.save_data['Parameter'].isin([param])]
                new_save_data.drop(['Parameter'], axis='columns', inplace=True)
                new_save_data.to_excel(writer, sheet_name=param, index=False)
                writer.save()
            writer.close()
            self.chart.save_chart(full_dir, project_dir)

        # сохранение проекта в БД
        params = ' '.join(self.params)
        self.saveproject_data = (date, self.project_state, self.path, params)
        data = self.newproject_data + self.saveproject_data
        check_db.save_project(self.expert_name, data)

        QMessageBox.about(self, 'Сохранение результатов', 'Результаты успешно сохранены')
        self.btn_save_results.setEnabled(False)
        self.check_draft.setEnabled(False)

    def report_ugt(self):
        res_list = [float(self.label_trl_result.text()),
                    float(self.label_mrl_result.text()),
                    float(self.label_erl_result.text()),
                    float(self.label_orl_result.text()),
                    float(self.label_crl_result.text())]
        results = []
        for i in range(len(self.parameters)):
            for param in self.params:
                if self.parameters[i] == param:
                    results.append(res_list[i])
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        data = {}
        for param in self.params:
            new_save_data = self.save_data.loc[self.save_data['Parameter'].isin([param])]
            new_save_data.drop(['Parameter'], axis='columns', inplace=True)
            data[param] = new_save_data
        self.pdf_data = (
            [date, self.project_num, self.expert_name, self.params, results,
             [self.tprl_min, self.label_main_tprl.text()]],
            data
        )
        new_report_ugt = ReportUgt(self.pdf_data, self.d1)
        new_report_ugt.set_data()

    def show_results(self, res):
        res_list = []
        for k_res, v_res in res.items():
            n = Decimal(f'{v_res}')
            v = n.quantize(Decimal('1.0'), rounding='ROUND_HALF_UP')
            if k_res == 'TRL':
                self.label_trl_result.setText(f'{v}')
            elif k_res == 'MRL':
                self.label_mrl_result.setText(f'{v}')
            elif k_res == 'ERL':
                self.label_erl_result.setText(f'{v}')
            elif k_res == 'ORL':
                self.label_orl_result.setText(f'{v}')
            elif k_res == 'CRL':
                self.label_crl_result.setText(f'{v}')
        show_res = res.copy()
        if len(self.params) < 5:
            self.tprl_average = '--'
            self.tprl_min = '--'
            self.label_tprl_average_result.setText(self.tprl_average)
            self.label_tprl_min_result.setText(self.tprl_min)
        else:
            while float(max(show_res.values())) - float(min(show_res.values())) >= 2:
                x = float(max(show_res.values()))
                for d3_k, d3_v in show_res.items():
                    if float(d3_v) == x:
                        d3_v = round(float(d3_v) - 1, 1)
                    show_res[d3_k] = str(d3_v)
            for new_v in show_res.values():
                res_list.append(float(new_v))
            self.tprl_average = float(sum(res_list) / len(res_list))
            number = Decimal(f'{self.tprl_average}')
            self.tprl_average = number.quantize(Decimal("1.0"), rounding='ROUND_HALF_UP')
            self.tprl_min = int(self.tprl_average)
            self.label_tprl_average_result.setText(str(self.tprl_average))
            self.label_tprl_min_result.setText(str(self.tprl_min))

    def show_risks(self):
        self.risk_param_tabs.clear()
        for param in self.params:
            self.risk_param_tab = QWidget()
            self.risk_param_tabs.addTab(self.risk_param_tab, param)
            self.risk_param_tabs.setCurrentIndex(self.params.index(param))
            self.risk_param_tabs.setTabEnabled(self.params.index(param), True)


    def show_help(self):
        self.help_dialog = HelpDialog(self)
        self.help_dialog.show()

    def closeEvent(self, event):
        if self.confirm_msg("Вы уверены, что хотите закрыть программу?"):
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
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    controller = Controller()  # Создаем экземпляр класса
    controller.show_splash()
    app.processEvents()
    sys.exit(app.exec_())
