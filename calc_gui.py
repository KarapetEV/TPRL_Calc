# -*- coding: utf-8 -*-

# Copyright 2020 Aleksey Karapyshev, Evgeniy Karapyshev ©
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppWindow(object):
    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.setWindowTitle("TPRL Calculator")
        AppWindow.setFixedSize(820, 685)
        AppWindow.setWindowIcon(QtGui.QIcon('.\img\\rzd.png'))
        self.frame_title = QtWidgets.QFrame(AppWindow)
        self.frame_title.setGeometry(QtCore.QRect(0, 0, 820, 70))
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.frame_title.setContentsMargins(0, 0, 0, 0)
        self.logo = QtWidgets.QLabel(self.frame_title)
        self.logo.setGeometry(QtCore.QRect(5, 10, 95, 50))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.labelCalc = QtWidgets.QLabel(self.frame_title)
        self.labelCalc.setGeometry(QtCore.QRect(100, 0, 720, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelCalc.setFont(font)
        self.labelCalc.setTextFormat(QtCore.Qt.RichText)
        self.labelCalc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCalc.setWordWrap(True)
        self.labelCalc.setObjectName("labelCalc")
        #-----------------------Создание вкладок---------------------------
        self.tabWidget = QtWidgets.QTabWidget(AppWindow)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 75, 820, 720))
        self.tabWidget.setObjectName("tabWidget")
        # -------------------------Create HELP Button-------------------
        self.btn_manual = QtWidgets.QPushButton(self.tabWidget)
        self.btn_manual.setGeometry(QtCore.QRect(770, 0, 45, 20))
        self.btn_manual.setObjectName("btn_manual")
        # -----------------------Вкладка проектов (новый)---------------------------
        self.tab_new_project = QtWidgets.QWidget()
        self.tab_new_project.setObjectName("tab_new_project")
        self.tabWidget.addTab(self.tab_new_project, "")
        self.label_user_name = QtWidgets.QLabel(self.tab_new_project)
        self.label_user_name.setGeometry(QtCore.QRect(50, 10, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        font.setBold(False)
        font.setWeight(25)
        self.label_user_name.setFont(font)
        self.label_user_name.setTextFormat(QtCore.Qt.RichText)
        self.label_user_name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.btn_change_user = QtWidgets.QPushButton(self.tab_new_project)
        self.btn_change_user.setGeometry(QtCore.QRect(580, 10, 190, 30))
        self.btn_change_user.setObjectName("btn_change_user")
        line_edit_style = '''
                    border: 1px solid red;
                    font-size: 14px;
                    '''
        self.enter_project_num = QtWidgets.QLineEdit()
        self.enter_project_num.setStyleSheet(line_edit_style)
        self.enter_project_date = QtWidgets.QLineEdit()
        self.enter_project_date.setStyleSheet(line_edit_style)
        self.enter_theme = QtWidgets.QLineEdit()
        self.enter_theme.setStyleSheet(line_edit_style)
        self.enter_initiator = QtWidgets.QLineEdit()
        self.enter_initiator.setStyleSheet(line_edit_style)
        self.enter_customer = QtWidgets.QLineEdit()
        self.enter_customer.setStyleSheet(line_edit_style)
        label_style = '''
                         border: none;
                         font-size: 14px;
                         font-weight: bold;
                         '''
        self.form = QtWidgets.QFormLayout()
        self.form.setSpacing(50)
        self.form.setContentsMargins(10, 100, 10, 0)
        self.form.addRow("&Номер проекта:", self.enter_project_num)
        self.form.labelForField(self.enter_project_num).setStyleSheet(label_style)
        self.form.addRow("&Дата проекта:", self.enter_project_date)
        self.form.labelForField(self.enter_project_date).setStyleSheet(label_style)
        self.form.addRow("&Тема проекта:", self.enter_theme)
        self.form.labelForField(self.enter_theme).setStyleSheet(label_style)
        self.form.addRow("&Инициатор проекта:", self.enter_initiator)
        self.form.labelForField(self.enter_initiator).setStyleSheet(label_style)
        self.form.addRow("&Заказчик по проекту:", self.enter_customer)
        self.form.labelForField(self.enter_customer).setStyleSheet(label_style)
        self.tab_new_project.setLayout(self.form)
        self.btn_new_project = QtWidgets.QPushButton(self.tab_new_project)
        self.btn_new_project.setGeometry(QtCore.QRect(310, 500, 200, 30))
        self.btn_new_project.setObjectName("btn_new_project")
        # -----------------------Вкладка проектов (черновики)---------------------------
        self.tab_user = QtWidgets.QWidget()
        self.tab_user.setObjectName("tab_user")
        self.tabWidget.addTab(self.tab_user, "")
        self.frame_user_tab = QtWidgets.QFrame(self.tab_user)
        self.frame_user_tab.setGeometry(QtCore.QRect(0, 0, 820, 580))
        self.frame_user_tab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_user_tab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_user_tab.setObjectName('frame_user_tab')
        self.label_user_name1 = QtWidgets.QLabel(self.frame_user_tab)
        self.label_user_name1.setGeometry(QtCore.QRect(50, 10, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(25)
        self.label_user_name1.setFont(font)
        self.label_user_name1.setTextFormat(QtCore.Qt.RichText)
        self.label_user_name1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.btn_change_user1 = QtWidgets.QPushButton(self.frame_user_tab)
        self.btn_change_user1.setGeometry(QtCore.QRect(580, 10, 190, 30))
        self.btn_change_user1.setObjectName("btn_change_user1")
        # Таблица черновиков
        self.projects_table = QtWidgets.QTableWidget(self.frame_user_tab)
        self.projects_table.setGeometry(QtCore.QRect(50, 50, 720, 470))
        self.projects_table.setContentsMargins(0, 0, 0, 0)
        self.projects_table.setObjectName('projects_table')
        self.projects_table.setColumnCount(7)
        self.projects_table.setRowCount(0)
        self.projects_table.verticalHeader().setVisible(False)

        # Заголовки таблицы черновиков
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table.setHorizontalHeaderItem(6, item)
        # Кнопка загрузки черновика
        self.btn_load_project = QtWidgets.QPushButton(self.frame_user_tab)
        self.btn_load_project.setGeometry(QtCore.QRect(130, 535, 150, 30))
        self.btn_load_project.setObjectName("btn_load_project")
        # Кнопка удаления проекта из черновиков
        self.btn_remove_project = QtWidgets.QPushButton(self.frame_user_tab)
        self.btn_remove_project.setGeometry(QtCore.QRect(540, 535, 150, 30))
        self.btn_remove_project.setObjectName("btn_remove_project")
        # -----------------------Вкладка проектов (завершенные)---------------------------
        self.tab_user2 = QtWidgets.QWidget()
        self.tab_user2.setObjectName("tab_user2")
        self.tabWidget.addTab(self.tab_user2, "")
        self.frame_user_tab2 = QtWidgets.QFrame(self.tab_user2)
        self.frame_user_tab2.setGeometry(QtCore.QRect(0, 0, 820, 580))
        self.frame_user_tab2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_user_tab2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_user_tab2.setObjectName('frame_user_tab')
        self.label_user_name2 = QtWidgets.QLabel(self.frame_user_tab2)
        self.label_user_name2.setGeometry(QtCore.QRect(50, 10, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(25)
        self.label_user_name2.setFont(font)
        self.label_user_name2.setTextFormat(QtCore.Qt.RichText)
        self.label_user_name2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.btn_change_user2 = QtWidgets.QPushButton(self.frame_user_tab2)
        self.btn_change_user2.setGeometry(QtCore.QRect(580, 10, 190, 30))
        self.btn_change_user2.setObjectName("btn_change_user2")
        # Таблица завершенных проектов
        self.projects_table2 = QtWidgets.QTableWidget(self.frame_user_tab2)
        self.projects_table2.setGeometry(QtCore.QRect(50, 50, 720, 470))
        self.projects_table2.setContentsMargins(0, 0, 0, 0)
        self.projects_table2.setObjectName('projects_table2')
        self.projects_table2.setColumnCount(7)
        self.projects_table.setRowCount(0)
        self.projects_table2.verticalHeader().setVisible(False)
        # Заголовки таблицы завершенных проектов
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.projects_table2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.projects_table2.setHorizontalHeaderItem(6, item)
        # Кнопка загрузки завершенного проекта
        self.btn_load_project2 = QtWidgets.QPushButton(self.frame_user_tab2)
        self.btn_load_project2.setGeometry(QtCore.QRect(335, 535, 150, 30))
        self.btn_load_project2.setObjectName("btn_load_project2")
        # -----------------------Вкладка калькулятора---------------------------
        self.tab_calc = QtWidgets.QWidget()
        self.tab_calc.setObjectName("tab_calc")
        self.tabWidget.addTab(self.tab_calc, "")
        self.frame_params = QtWidgets.QFrame(self.tab_calc)
        self.frame_params.setGeometry(QtCore.QRect(0, 0, 820, 150))
        self.frame_params.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_params.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_params.setObjectName('frame_params')
        self.group_params = QtWidgets.QGroupBox(self.frame_params)
        self.group_params.setEnabled(True)
        self.group_params.setGeometry(QtCore.QRect(10, 10, 340, 140))
        self.group_params.setObjectName("frame_params")
        self.check_trl = QtWidgets.QCheckBox(self.group_params)
        self.check_trl.setGeometry(QtCore.QRect(20, 20, 240, 17))
        self.check_trl.setObjectName("check_trl")
        self.check_trl.setChecked(False)
        self.check_mrl = QtWidgets.QCheckBox(self.group_params)
        self.check_mrl.setGeometry(QtCore.QRect(20, 45, 240, 17))
        self.check_mrl.setObjectName("check_mrl")
        self.check_mrl.setChecked(False)
        self.check_erl = QtWidgets.QCheckBox(self.group_params)
        self.check_erl.setGeometry(QtCore.QRect(20, 70, 240, 17))
        self.check_erl.setObjectName("check_erl")
        self.check_erl.setChecked(False)
        self.check_orl = QtWidgets.QCheckBox(self.group_params)
        self.check_orl.setGeometry(QtCore.QRect(20, 95, 240, 17))
        self.check_orl.setObjectName("check_orl")
        self.check_orl.setChecked(False)
        self.check_crl = QtWidgets.QCheckBox(self.group_params)
        self.check_crl.setGeometry(QtCore.QRect(20, 120, 240, 17))
        self.check_crl.setObjectName("check_crl")
        self.check_crl.setChecked(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        font.setBold(False)
        font.setWeight(25)
        self.label_num_calcTab = QtWidgets.QLabel(self.frame_params)
        self.label_num_calcTab.setGeometry(QtCore.QRect(380, 30, 120, 20))
        self.label_num_calcTab.setObjectName("label_num_calcTab")
        self.label_num_calcTab.setFont(font)
        self.num_calcTab = QtWidgets.QLabel(self.frame_params)
        self.num_calcTab.setGeometry(QtCore.QRect(510, 30, 250, 20))
        self.num_calcTab.setObjectName("num_calcTab")
        self.num_calcTab.setFont(font)
        self.label_user_calcTab = QtWidgets.QLabel(self.frame_params)
        self.label_user_calcTab.setGeometry(QtCore.QRect(380, 60, 120, 20))
        self.label_user_calcTab.setObjectName("label_user_calcTab")
        self.label_user_calcTab.setFont(font)
        self.user_calcTab = QtWidgets.QLabel(self.frame_params)
        self.user_calcTab.setGeometry(QtCore.QRect(510, 60, 300, 20))
        self.user_calcTab.setObjectName("user_calcTab")
        self.user_calcTab.setFont(font)
        self.btn_set_params = QtWidgets.QPushButton(self.frame_params)
        self.btn_set_params.setGeometry(QtCore.QRect(475, 110, 200, 30))
        self.btn_set_params.setObjectName("btn_set_params")
        # -------------Фрейм с вкладками вопросов по параметрам---------------------
        self.frame_tasks = QtWidgets.QFrame(self.tab_calc)
        self.frame_tasks.setGeometry(QtCore.QRect(0, 155, 820, 463))
        self.frame_tasks.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tasks.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tasks.setObjectName("frame_tasks")
        self.param_tabs = QtWidgets.QTabWidget(self.frame_tasks)
        self.param_tabs.setEnabled(True)
        self.param_tabs.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.param_tabs.setObjectName("param_tabs")

        self.btn_calculate = QtWidgets.QPushButton(self.frame_tasks)
        self.btn_calculate.setGeometry(QtCore.QRect(102, 390, 180, 30))
        font = QtGui.QFont('fonts/RussianRail/RussianRail_Regular.otf')
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_calculate.setFont(font)
        self.btn_calculate.setObjectName("btn_calculate")
        self.btn_calculate.setEnabled(False)
        self.btn_reset_tasks = QtWidgets.QPushButton(self.frame_tasks)
        self.btn_reset_tasks.setGeometry(QtCore.QRect(486, 390, 180, 30))
        font = QtGui.QFont('fonts/RussianRail/RussianRail_Regular.otf')
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_reset_tasks.setFont(font)
        self.btn_reset_tasks.setObjectName("btn_reset_tasks")
        self.btn_reset_tasks.setEnabled(False)
        #----------------------Вкладка результатов-----------------------------
        self.tab_results = QtWidgets.QWidget()
        self.tab_results.setObjectName("tab_results")
        self.tabWidget.addTab(self.tab_results, "")
        self.frame_results = QtWidgets.QFrame(self.tab_results)
        self.frame_results.setEnabled(False)
        self.frame_results.setGeometry(QtCore.QRect(0, 0, 383, 250))
        self.frame_results.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_results.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_results.setObjectName("frame_results")
        self.labelProject = QtWidgets.QLabel(self.frame_results)
        self.labelProject.setGeometry(QtCore.QRect(10, 10, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelProject.setObjectName("labelProject")
        self.label_project_num = QtWidgets.QLabel(self.frame_results)
        self.label_project_num.setGeometry(QtCore.QRect(180, 10, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_project_num.setFont(font)
        self.label_project_num.setObjectName("label_project_num")
        self.label_expert = QtWidgets.QLabel(self.frame_results)
        self.label_expert.setGeometry(QtCore.QRect(10, 45, 85, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_expert.setFont(font)
        self.label_expert.setText("Эксперт:")
        self.label_expert.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_expert.setObjectName("label_expert")
        self.label_expert_name = QtWidgets.QLabel(self.frame_results)
        self.label_expert_name.setGeometry(QtCore.QRect(100, 45, 300, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_expert_name.setFont(font)
        self.label_expert_name.setText("Иванов И.И.")
        self.label_expert_name.setWordWrap(True)
        self.label_expert_name.setObjectName("label_project_num")
        # ----------------------TPRL_min_label-----------------------
        self.label_tprl_min = QtWidgets.QLabel(self.frame_results)
        self.label_tprl_min.setGeometry(QtCore.QRect(10, 95, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_tprl_min.setFont(font)
        self.label_tprl_min.setObjectName("label_tprl_min")
        # ----------------------TPRL_min_result-----------------------
        self.label_tprl_min_result = QtWidgets.QLabel(self.frame_results)
        self.label_tprl_min_result.setGeometry(QtCore.QRect(130, 95, 40, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_tprl_min_result.setFont(font)
        self.label_tprl_min_result.setObjectName("label_tprl_min_result")
        # ----------------------TPRL_average_label-----------------------
        self.label_tprl_average = QtWidgets.QLabel(self.frame_results)
        self.label_tprl_average.setGeometry(QtCore.QRect(10, 135, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_tprl_average.setFont(font)
        self.label_tprl_average.setObjectName("label_tprl_average")
        # ----------------------TPRL_average_result-----------------------
        self.label_tprl_average_result = QtWidgets.QLabel(self.frame_results)
        self.label_tprl_average_result.setGeometry(QtCore.QRect(130, 135, 40, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_tprl_average_result.setFont(font)
        self.label_tprl_average_result.setObjectName("label_tprl_average_result")

        self.trl = QtWidgets.QLabel(self.frame_results)
        self.trl.setGeometry(QtCore.QRect(70, 180, 30, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trl.setFont(font)
        self.trl.setObjectName("trl")
        self.label_trl_result = QtWidgets.QLabel(self.frame_results)
        self.label_trl_result.setGeometry(QtCore.QRect(68, 200, 32, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_trl_result.setFont(font)
        self.label_trl_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_trl_result.setLineWidth(2)
        self.label_trl_result.setMidLineWidth(1)
        self.label_trl_result.setTextFormat(QtCore.Qt.PlainText)
        self.label_trl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_trl_result.setObjectName("label_trl_result")
        self.mrl = QtWidgets.QLabel(self.frame_results)
        self.mrl.setGeometry(QtCore.QRect(130, 180, 30, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mrl.setFont(font)
        self.mrl.setObjectName("mrl")
        self.label_mrl_result = QtWidgets.QLabel(self.frame_results)
        self.label_mrl_result.setGeometry(QtCore.QRect(128, 200, 32, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_mrl_result.setFont(font)
        self.label_mrl_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_mrl_result.setLineWidth(2)
        self.label_mrl_result.setMidLineWidth(1)
        self.label_mrl_result.setTextFormat(QtCore.Qt.PlainText)
        self.label_mrl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mrl_result.setObjectName("label_mrl_result")
        self.erl = QtWidgets.QLabel(self.frame_results)
        self.erl.setGeometry(QtCore.QRect(190, 180, 30, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.erl.setFont(font)
        self.erl.setObjectName("erl")
        self.label_erl_result = QtWidgets.QLabel(self.frame_results)
        self.label_erl_result.setGeometry(QtCore.QRect(188, 200, 32, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_erl_result.setFont(font)
        self.label_erl_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_erl_result.setLineWidth(2)
        self.label_erl_result.setMidLineWidth(1)
        self.label_erl_result.setTextFormat(QtCore.Qt.PlainText)
        self.label_erl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_erl_result.setObjectName("label_erl_result")
        self.orl = QtWidgets.QLabel(self.frame_results)
        self.orl.setGeometry(QtCore.QRect(250, 180, 30, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.orl.setFont(font)
        self.orl.setObjectName("orl")
        self.label_orl_result = QtWidgets.QLabel(self.frame_results)
        self.label_orl_result.setGeometry(QtCore.QRect(248, 200, 32, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_orl_result.setFont(font)
        self.label_orl_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_orl_result.setLineWidth(2)
        self.label_orl_result.setMidLineWidth(1)
        self.label_orl_result.setTextFormat(QtCore.Qt.PlainText)
        self.label_orl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_orl_result.setObjectName("label_orl_result")
        self.crl = QtWidgets.QLabel(self.frame_results)
        self.crl.setGeometry(QtCore.QRect(310, 180, 30, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.crl.setFont(font)
        self.crl.setObjectName("crl")
        self.label_crl_result = QtWidgets.QLabel(self.frame_results)
        self.label_crl_result.setGeometry(QtCore.QRect(308, 200, 32, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_crl_result.setFont(font)
        self.label_crl_result.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_crl_result.setLineWidth(2)
        self.label_crl_result.setMidLineWidth(1)
        self.label_crl_result.setTextFormat(QtCore.Qt.PlainText)
        self.label_crl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_crl_result.setObjectName("label_crl_result")
        self.line_vertical = QtWidgets.QFrame(self.tab_results)
        self.line_vertical.setGeometry(QtCore.QRect(410, 0, 2, 230))
        self.line_vertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_vertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_vertical.setObjectName("line_vertical")
        self.frame_graph = QtWidgets.QFrame(self.tab_results)
        self.frame_graph.setGeometry(QtCore.QRect(412, 0, 408, 230))
        self.frame_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graph.setObjectName("frame_graph")
        self.lay = QtWidgets.QVBoxLayout(self.frame_graph)
        self.lay.setContentsMargins(0, 10, 40, 0)
        self.line_horizontal = QtWidgets.QFrame(self.tab_results)
        self.line_horizontal.setGeometry(QtCore.QRect(5, 232, 820, 2))
        self.line_horizontal.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horizontal.setObjectName("line_horizontal")
        #-----------------------Frame_TPRL_results----------------------
        self.frame_tprl_results = QtWidgets.QFrame(self.tab_results)
        self.frame_tprl_results.setGeometry(QtCore.QRect(5, 235, 815, 345))
        self.frame_tprl_results.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tprl_results.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tprl_results.setObjectName('frame_tprl_results')
        #------------------------Label_Main_TPRL-------------------------
        self.label_main_tprl = QtWidgets.QLabel(self.frame_tprl_results)
        self.label_main_tprl.setGeometry(QtCore.QRect(0, 0, 805, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_main_tprl.setFont(font)
        self.label_main_tprl.setWordWrap(True)
        self.label_main_tprl.setObjectName('label_main_tprl')
        # -----------------------Table_TPRL_results----------------------
        self.table_tprl_results = QtWidgets.QTableWidget(self.frame_tprl_results)
        self.table_tprl_results.setGeometry(QtCore.QRect(0, 55, 805, 260))
        self.table_tprl_results.setContentsMargins(0, 0, 0, 0)
        self.table_tprl_results.setObjectName('table_tprl_results')
        self.table_tprl_results.horizontalHeader().setVisible(False)
        self.table_tprl_results.verticalHeader().setVisible(False)
        #-------------------------Draft_CheckBox-------------------------
        self.check_draft = QtWidgets.QCheckBox(self.frame_tprl_results)
        self.check_draft.setGeometry(QtCore.QRect(335, 310, 180, 30))
        self.check_draft.setObjectName("check_draft")
        self.check_draft.setChecked(False)
        #----------------------Save_results Button-----------------------
        self.btn_save_results = QtWidgets.QPushButton(self.frame_tprl_results)
        self.btn_save_results.setGeometry(QtCore.QRect(150, 310, 180, 30))
        font = QtGui.QFont('fonts/RussianRail/RussianRail_Regular.otf')
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_save_results.setFont(font)
        self.btn_save_results.setObjectName("btn_save_results")

        self.btn_pdf = QtWidgets.QPushButton(self.frame_tprl_results)
        self.btn_pdf.setGeometry(QtCore.QRect(480, 310, 180, 30))
        font = QtGui.QFont('fonts/RussianRail/RussianRail_Regular.otf')
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_pdf.setFont(font)
        self.btn_pdf.setObjectName("btn_pdf")

        self.tabWidget.raise_()
        self.labelCalc.raise_()

        self.retranslateUi(AppWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)

    def retranslateUi(self, AppWindow):
        _translate = QtCore.QCoreApplication.translate
        AppWindow.setWindowTitle(_translate("AppWindow", "TPRL Calculator"))
        self.labelCalc.setText(_translate("AppWindow", "Расчёт уровня зрелости инновационного продукта/технологии к внедрению в ОАО «РЖД»"))
        self.btn_manual.setText(_translate("AppWindow", "Справка"))
        self.btn_change_user.setText(_translate("AppWindow", "Сменить пользователя"))
        self.btn_change_user1.setText(_translate("AppWindow", "Сменить пользователя"))
        self.btn_change_user2.setText(_translate("AppWindow", "Сменить пользователя"))
        self.btn_new_project.setText(_translate("AppWindow", "Начать новый проект"))
        self.btn_load_project.setText(_translate("AppWindow", "Загрузить проект"))
        self.btn_remove_project.setText(_translate("AppWindow", "Удалить проект"))
        self.btn_load_project2.setText(_translate("AppWindow", "Загрузить проект"))
        # self.btn_new_project2.setText(_translate("AppWindow", "Новый проект"))
        self.group_params.setTitle(_translate("AppWindow", "Параметры оценки"))
        self.check_trl.setText(_translate("AppWindow", "Технологическая готовность (TRL)"))
        self.check_mrl.setText(_translate("AppWindow", "Производственная готовность (MRL)"))
        self.check_erl.setText(_translate("AppWindow", "Инженерная готовность (ERL)"))
        self.check_orl.setText(_translate("AppWindow", "Организационная готовность (ORL)"))
        self.check_crl.setText(_translate("AppWindow", "Коммерческая готовность (СRL)"))
        self.label_num_calcTab.setText(_translate("AppWindow", "Номер проекта:"))
        self.label_user_calcTab.setText(_translate("AppWindow", "Эксперт:"))
        self.btn_set_params.setText(_translate("AppWindow", "Установить параметры"))
        self.labelProject.setText(_translate("AppWindow", "Номер проекта:"))
        self.label_tprl_min.setText(_translate("AppWindow", "TPRLmin:"))
        self.label_tprl_average.setText(_translate("AppWindow", "TPRLav:"))
        self.label_main_tprl.setText(_translate("AppWindow", ""))
        self.check_draft.setText(_translate("AppWindow", "черновик"))
        self.trl.setText(_translate("AppWindow", "TRL"))
        self.label_trl_result.setText(_translate("AppWindow", "0"))
        self.mrl.setText(_translate("AppWindow", "MRL"))
        self.label_mrl_result.setText(_translate("AppWindow", "0"))
        self.erl.setText(_translate("AppWindow", "ERL"))
        self.label_erl_result.setText(_translate("AppWindow", "0"))
        self.orl.setText(_translate("AppWindow", "ORL"))
        self.label_orl_result.setText(_translate("AppWindow", "0"))
        self.crl.setText(_translate("AppWindow", "CRL"))
        self.label_crl_result.setText(_translate("AppWindow", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_new_project), _translate("AppWindow", "Новый"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user), _translate("AppWindow", "Черновики"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user2), _translate("AppWindow", "Завершенные"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calc), _translate("AppWindow", "Калькулятор"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_results), _translate("AppWindow", "Результат"))
        self.btn_calculate.setText(_translate("AppWindow", "Рассчитать"))
        self.btn_reset_tasks.setText(_translate("AppWindow", "Сбросить задачи"))
        self.btn_save_results.setText(_translate("AppWindow", "Сохранить"))
        self.btn_pdf.setText(_translate("AppWindow", "Создать заключение"))
        self.enter_project_num.setPlaceholderText(_translate("AppWindow", 'Введите номер проекта...'))
        self.enter_project_date.setPlaceholderText(_translate("AppWindow", 'Введите дату регистрации проекта...'))
        self.enter_theme.setPlaceholderText(_translate("AppWindow", 'Введите тему проекта...'))
        self.enter_initiator.setPlaceholderText(_translate("AppWindow", 'Введите наименование инициатора...'))
        self.enter_customer.setPlaceholderText(_translate("AppWindow", 'Введите наименование заказчика...'))
        # Заголовки таблицы "Черновики"
        item = self.projects_table.horizontalHeaderItem(0)
        item.setText(_translate("AppWindow", "№ п/п"))
        item = self.projects_table.horizontalHeaderItem(1)
        item.setText(_translate("AppWindow", "УИН проекта"))
        item = self.projects_table.horizontalHeaderItem(2)
        item.setText(_translate("AppWindow", "Дата проекта"))
        item = self.projects_table.horizontalHeaderItem(3)
        item.setText(_translate("AppWindow", "Тема"))
        item = self.projects_table.horizontalHeaderItem(4)
        item.setText(_translate("AppWindow", "Инициатор"))
        item = self.projects_table.horizontalHeaderItem(5)
        item.setText(_translate("AppWindow", "Заказчик"))
        item = self.projects_table.horizontalHeaderItem(6)
        item.setText(_translate("AppWindow", "Дата оценки"))
        # Заголовки таблицы "Завершенные"
        item = self.projects_table2.horizontalHeaderItem(0)
        item.setText(_translate("AppWindow", "№ п/п"))
        item = self.projects_table2.horizontalHeaderItem(1)
        item.setText(_translate("AppWindow", "УИН проекта"))
        item = self.projects_table2.horizontalHeaderItem(2)
        item.setText(_translate("AppWindow", "Дата проекта"))
        item = self.projects_table2.horizontalHeaderItem(3)
        item.setText(_translate("AppWindow", "Тема"))
        item = self.projects_table2.horizontalHeaderItem(4)
        item.setText(_translate("AppWindow", "Инициатор"))
        item = self.projects_table2.horizontalHeaderItem(5)
        item.setText(_translate("AppWindow", "Заказчик"))
        item = self.projects_table2.horizontalHeaderItem(6)
        item.setText(_translate("AppWindow", "Дата оценки"))
