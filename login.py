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

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.setWindowTitle("Авторизация пользователя")
        Login.setWindowIcon(QtGui.QIcon('.\img\\rzd.png'))
        Login.setFixedSize(320, 250)
        Login.setWindowFlags(
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
            )
        self.main_frame = QtWidgets.QFrame(Login)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 320, 250))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setContentsMargins(0, 0, 0, 0)
        self.label_login_title = QtWidgets.QLabel(self.main_frame)
        self.label_login_title.setGeometry(QtCore.QRect(5, 0, 310, 40))
        self.label_login_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login_title.setObjectName("label_login_title")
        self.label_login_title.setStyleSheet('''
                                            font-weight: bold;
                                            font-size: 16px;
                                            ''')
        self.comboBox_users = QtWidgets.QComboBox(self.main_frame)
        self.comboBox_users.setObjectName("comboBox_users")
        self.comboBox_users.setGeometry(QtCore.QRect(5, 70, 310, 30))
        self.comboBox_users.setStyleSheet('''
                                            border-radius: 3px;
                                            border: 1px solid red;
                                            font-size: 14px;
                                            ''')
        self.lineEdit_password = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setGeometry(QtCore.QRect(5, 130, 310, 30))
        self.lineEdit_password.setStyleSheet('''
                                            border-radius: 3px;
                                            border: 1px solid red;
                                            font-size: 14px;
                                            ''')
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_choose_user = QtWidgets.QPushButton(self.main_frame)
        self.btn_choose_user.setObjectName("btn_choose_user")
        self.btn_choose_user.setGeometry(QtCore.QRect(5, 205, 150, 30))
        self.btn_new_user = QtWidgets.QPushButton(self.main_frame)
        self.btn_new_user.setObjectName("btn_new_user")
        self.btn_new_user.setGeometry(QtCore.QRect(165, 205, 150, 30))

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Авторизация"))
        self.label_login_title.setText(_translate("Login", "Выбор пользователя"))
        self.lineEdit_password.setPlaceholderText(_translate("Login", "Введите пароль..."))
        self.btn_choose_user.setText(_translate("Login", "Выбрать"))
        self.btn_new_user.setText(_translate("Login", "Создать нового"))
