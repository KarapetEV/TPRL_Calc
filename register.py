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


class Ui_Register(object):
    def setupUi(self, Register):
        Register.setObjectName("Register")
        Register.setWindowTitle("Регистрация пользователя")
        Register.setWindowIcon(QtGui.QIcon('.\img\\rzd.png'))
        Register.setFixedSize(320, 250)
        Register.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.main_frame = QtWidgets.QFrame(Register)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 320, 250))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setContentsMargins(0, 0, 0, 0)
        self.label_register_title = QtWidgets.QLabel(self.main_frame)
        self.label_register_title.setGeometry(QtCore.QRect(5, 0, 310, 40))
        self.label_register_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_register_title.setObjectName("label_register_title")
        self.label_register_title.setStyleSheet('''
                                                   font-weight: bold;
                                                   font-size: 16px;
                                                   ''')
        self.lineEdit_login_create = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_login_create.setObjectName("lineEdit_login_create")
        self.lineEdit_login_create.setGeometry(QtCore.QRect(5, 60, 310, 30))
        self.lineEdit_login_create.setStyleSheet('''
                                                    border-radius: 3px;
                                                    border: 1px solid red;
                                                    font-size: 14px;
                                                    ''')
        self.lineEdit_password_create = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_password_create.setObjectName("lineEdit_password_create")
        self.lineEdit_password_create.setGeometry(QtCore.QRect(5, 110, 310, 30))
        self.lineEdit_password_create.setStyleSheet('''
                                                       border-radius: 3px;
                                                       border: 1px solid red;
                                                       font-size: 14px;
                                                       ''')
        self.lineEdit_password_create.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_confirm = QtWidgets.QLineEdit(self.main_frame)
        self.lineEdit_password_confirm.setObjectName("lineEdit_password_confirm")
        self.lineEdit_password_confirm.setGeometry(QtCore.QRect(5, 160, 310, 30))
        self.lineEdit_password_confirm.setStyleSheet('''
                                                        border-radius: 3px;
                                                        border: 1px solid red;
                                                        font-size: 14px;
                                                        ''')
        self.lineEdit_password_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_register = QtWidgets.QPushButton(self.main_frame)
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setGeometry(QtCore.QRect(5, 205, 150, 30))
        self.btn_back = QtWidgets.QPushButton(self.main_frame)
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setGeometry(QtCore.QRect(165, 205, 150, 30))

        self.retranslateUi(Register)
        QtCore.QMetaObject.connectSlotsByName(Register)

    def retranslateUi(self, Register):
        _translate = QtCore.QCoreApplication.translate
        Register.setWindowTitle(_translate("Register", "Регистрация пользователя"))
        self.label_register_title.setText(_translate("Register", "Регистрация пользователя"))
        self.lineEdit_login_create.setPlaceholderText(_translate("Register", "Введите ФИО..."))
        self.lineEdit_password_create.setPlaceholderText(_translate("Register", "Введите пароль..."))
        self.lineEdit_password_confirm.setPlaceholderText(_translate("Register", "Подтвердите пароль..."))
        self.btn_register.setText(_translate("Register", "Зарегистрировать"))
        self.btn_back.setText(_translate("Register", "Назад"))
