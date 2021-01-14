# -*- coding: utf-8 -*-

# Copyright 2020 Aleksey Karapyshev, Evgeniy Karapyshev ©
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppWindow(object):
    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.setWindowTitle("TPRL Calculator")
        AppWindow.setFixedSize(820, 685)
        AppWindow.setWindowIcon(QtGui.QIcon('img/rzd.png'))
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
        # -----------------------Создание вкладок---------------------------
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
        self.label_user_name.setGeometry(QtCore.QRect(50, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(True)
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
        # # -----------------------Вкладка проектов (черновики)---------------------------
        # self.tab_user = QtWidgets.QWidget()
        # self.tab_user.setObjectName("tab_user")
        # self.tabWidget.addTab(self.tab_user, "")
        # self.frame_user_tab = QtWidgets.QFrame(self.tab_user)
        # self.frame_user_tab.setGeometry(QtCore.QRect(0, 0, 820, 580))
        # self.frame_user_tab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_user_tab.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_user_tab.setObjectName('frame_user_tab')
        # self.label_user_name1 = QtWidgets.QLabel(self.frame_user_tab)
        # self.label_user_name1.setGeometry(QtCore.QRect(50, 10, 200, 30))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # font.setBold(False)
        # font.setWeight(25)
        # self.label_user_name1.setFont(font)
        # self.label_user_name1.setTextFormat(QtCore.Qt.RichText)
        # self.label_user_name1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # self.btn_change_user1 = QtWidgets.QPushButton(self.frame_user_tab)
        # self.btn_change_user1.setGeometry(QtCore.QRect(580, 10, 190, 30))
        # self.btn_change_user1.setObjectName("btn_change_user1")
        # self.projects_table = QtWidgets.QTableWidget(self.frame_user_tab)
        # self.projects_table.setGeometry(QtCore.QRect(50, 50, 720, 470))
        # self.btn_load_project = QtWidgets.QPushButton(self.frame_user_tab)
        # self.btn_load_project.setGeometry(QtCore.QRect(335, 535, 150, 30))
        # self.btn_load_project.setObjectName("btn_load_project")
        # # -----------------------Вкладка проектов (завершенные)---------------------------
        # self.tab_user2 = QtWidgets.QWidget()
        # self.tab_user2.setObjectName("tab_user2")
        # self.tabWidget.addTab(self.tab_user2, "")
        # self.frame_user_tab2 = QtWidgets.QFrame(self.tab_user2)
        # self.frame_user_tab2.setGeometry(QtCore.QRect(0, 0, 820, 580))
        # self.frame_user_tab2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_user_tab2.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_user_tab2.setObjectName('frame_user_tab')
        # self.label_user_name2 = QtWidgets.QLabel(self.frame_user_tab2)
        # self.label_user_name2.setGeometry(QtCore.QRect(50, 10, 200, 30))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # font.setBold(False)
        # font.setWeight(25)
        # self.label_user_name2.setFont(font)
        # self.label_user_name2.setTextFormat(QtCore.Qt.RichText)
        # self.label_user_name2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # self.btn_change_user2 = QtWidgets.QPushButton(self.frame_user_tab2)
        # self.btn_change_user2.setGeometry(QtCore.QRect(580, 10, 190, 30))
        # self.btn_change_user2.setObjectName("btn_change_user2")
        # self.projects_table2 = QtWidgets.QTableWidget(self.frame_user_tab2)
        # self.projects_table2.setGeometry(QtCore.QRect(50, 50, 720, 470))
        # self.btn_load_project2 = QtWidgets.QPushButton(self.frame_user_tab2)
        # self.btn_load_project2.setGeometry(QtCore.QRect(335, 535, 150, 30))
        # self.btn_load_project2.setObjectName("btn_load_project2")
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
        self.check_trl.setChecked(True)
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
        # self.group_types = QtWidgets.QGroupBox(self.frame_params)
        # self.group_types.setGeometry(QtCore.QRect(400, 10, 330, 90))
        # self.group_types.setObjectName("frame_types")
        # self.radio_hard = QtWidgets.QRadioButton(self.group_types)
        # self.radio_hard.setGeometry(QtCore.QRect(10, 20, 211, 17))
        # self.radio_hard.setObjectName("radio_hard")
        # self.radio_hard.setChecked(True)
        # self.radio_soft = QtWidgets.QRadioButton(self.group_types)
        # self.radio_soft.setGeometry(QtCore.QRect(10, 45, 261, 17))
        # self.radio_soft.setObjectName("radio_soft")
        # self.radio_both = QtWidgets.QRadioButton(self.group_types)
        # self.radio_both.setGeometry(QtCore.QRect(10, 70, 261, 17))
        # self.radio_both.setAutoRepeat(False)
        # self.radio_both.setObjectName("radio_both")
        font = QtGui.QFont()
        font.setPixelSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_ugt1 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt1.setEnabled(False)
        self.label_ugt1.setGeometry(QtCore.QRect(457, 35, 15, 25))
        self.label_ugt1.setFont(font)
        self.label_ugt1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt1.setObjectName("label_ugt1")
        self.label_ugt2 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt2.setEnabled(False)
        self.label_ugt2.setGeometry(QtCore.QRect(487, 35, 15, 25))
        self.label_ugt2.setFont(font)
        self.label_ugt2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt2.setObjectName("label_ugt2")
        self.label_ugt3 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt3.setEnabled(False)
        self.label_ugt3.setGeometry(QtCore.QRect(517, 35, 15, 25))
        self.label_ugt3.setFont(font)
        self.label_ugt3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt3.setObjectName("label_ugt3")
        self.label_ugt4 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt4.setEnabled(False)
        self.label_ugt4.setGeometry(QtCore.QRect(547, 35, 15, 25))
        self.label_ugt4.setFont(font)
        self.label_ugt4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt4.setObjectName("label_ugt4")
        self.label_ugt5 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt5.setEnabled(False)
        self.label_ugt5.setGeometry(QtCore.QRect(577, 35, 15, 25))
        self.label_ugt5.setFont(font)
        self.label_ugt5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt5.setObjectName("label_ugt5")
        self.label_ugt6 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt6.setEnabled(False)
        self.label_ugt6.setGeometry(QtCore.QRect(607, 35, 15, 25))
        self.label_ugt6.setFont(font)
        self.label_ugt6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt6.setObjectName("label_ugt6")
        self.label_ugt7 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt7.setEnabled(False)
        self.label_ugt7.setGeometry(QtCore.QRect(637, 35, 15, 25))
        self.label_ugt7.setFont(font)
        self.label_ugt7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt7.setObjectName("label_ugt7")
        self.label_ugt8 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt8.setEnabled(False)
        self.label_ugt8.setGeometry(QtCore.QRect(667, 35, 15, 25))
        self.label_ugt8.setFont(font)
        self.label_ugt8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt8.setObjectName("label_ugt8")
        self.label_ugt9 = QtWidgets.QLabel(self.frame_params)
        self.label_ugt9.setEnabled(False)
        self.label_ugt9.setGeometry(QtCore.QRect(697, 35, 15, 25))
        self.label_ugt9.setFont(font)
        self.label_ugt9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ugt9.setObjectName("label_ugt9")
        self.ugtSlider = QtWidgets.QSlider(self.frame_params)
        self.ugtSlider.setEnabled(True)
        self.ugtSlider.setGeometry(QtCore.QRect(460, 60, 250, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ugtSlider.setFont(font)
        self.ugtSlider.setTabletTracking(False)
        self.ugtSlider.setAutoFillBackground(False)
        self.ugtSlider.setMaximum(8)
        self.ugtSlider.setPageStep(9)
        self.ugtSlider.setProperty("value", 0)
        self.ugtSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ugtSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.ugtSlider.setTickInterval(0)
        self.ugtSlider.setObjectName("ugtSlider")
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
        self.tab_trl_tasks = QtWidgets.QWidget()
        self.tab_trl_tasks.setObjectName("tab_trl_tasks")
        self.param_tabs.addTab(self.tab_trl_tasks, "")
        self.trl_tasks = QtWidgets.QTreeWidget(self.tab_trl_tasks)
        self.trl_tasks.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.trl_tasks.setObjectName("trl_tasks")
        self.tab_mrl_tasks = QtWidgets.QWidget()
        self.tab_mrl_tasks.setObjectName("tab_mrl_tasks")
        self.param_tabs.addTab(self.tab_mrl_tasks, "")
        self.mrl_tasks = QtWidgets.QTreeWidget(self.tab_mrl_tasks)
        self.mrl_tasks.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.mrl_tasks.setObjectName("mrl_tasks")
        self.tab_erl_tasks = QtWidgets.QWidget()
        self.tab_erl_tasks.setObjectName("tab_erl_tasks")
        self.param_tabs.addTab(self.tab_erl_tasks, "")
        self.erl_tasks = QtWidgets.QTreeWidget(self.tab_erl_tasks)
        self.erl_tasks.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.erl_tasks.setObjectName("erl_tasks")
        self.tab_orl_tasks = QtWidgets.QWidget()
        self.tab_orl_tasks.setObjectName("tab_orl_tasks")
        self.param_tabs.addTab(self.tab_orl_tasks, "")
        self.orl_tasks = QtWidgets.QTreeWidget(self.tab_orl_tasks)
        self.orl_tasks.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.orl_tasks.setObjectName("orl_tasks")
        self.tab_crl_tasks = QtWidgets.QWidget()
        self.tab_crl_tasks.setObjectName("tab_crl_tasks")
        self.param_tabs.addTab(self.tab_crl_tasks, "")
        self.crl_tasks = QtWidgets.QTreeWidget(self.tab_crl_tasks)
        self.crl_tasks.setGeometry(QtCore.QRect(0, 0, 815, 380))
        self.crl_tasks.setObjectName("crl_tasks")
        self.btn_calculate = QtWidgets.QPushButton(self.frame_tasks)
        self.btn_calculate.setGeometry(QtCore.QRect(102, 390, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_calculate.setFont(font)
        self.btn_calculate.setObjectName("btn_calculate")
        self.btn_calculate.setEnabled(False)
        self.btn_reset_tasks = QtWidgets.QPushButton(self.frame_tasks)
        self.btn_reset_tasks.setGeometry(QtCore.QRect(486, 390, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_reset_tasks.setFont(font)
        self.btn_reset_tasks.setObjectName("btn_reset_tasks")
        self.btn_reset_tasks.setEnabled(False)
        # ----------------------Вкладка результатов-----------------------------
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
        self.labelProject.setGeometry(QtCore.QRect(10, 15, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.labelProject.setObjectName("labelProject")
        self.label_project_num = QtWidgets.QLabel(self.frame_results)
        self.label_project_num.setGeometry(QtCore.QRect(180, 15, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_project_num.setFont(font)
        self.label_project_num.setObjectName("label_project_num")
        self.label_expert = QtWidgets.QLabel(self.frame_results)
        self.label_expert.setGeometry(QtCore.QRect(10, 55, 85, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_expert.setFont(font)
        self.label_expert.setText("Эксперт:")
        self.label_expert.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_expert.setObjectName("label_expert")
        self.label_expert_name = QtWidgets.QLabel(self.frame_results)
        self.label_expert_name.setGeometry(QtCore.QRect(100, 55, 250, 30))
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
        # self.save_graph_btn = QtWidgets.QPushButton(self.frame_graph)
        # self.save_graph_btn.setStyleSheet('background: #f3f3f3;')
        # self.save_graph_btn.setGeometry(QtCore.QRect(365, 190, 30, 30))
        # self.save_graph_btn.setContentsMargins(0, 0, 0, 0)
        # self.save_graph_btn.setIcon(QtGui.QIcon('.\img\\save_chart.png'))
        # self.save_graph_btn.setIconSize(QtCore.QSize(30, 30))
        # self.save_graph_btn.setToolTip("Сохранить график")
        # self.save_graph_btn.setEnabled(False)
        self.lay = QtWidgets.QVBoxLayout(self.frame_graph)
        self.lay.setContentsMargins(0, 0, 40, 0)
        self.line_horizontal = QtWidgets.QFrame(self.tab_results)
        self.line_horizontal.setGeometry(QtCore.QRect(5, 232, 820, 2))
        self.line_horizontal.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horizontal.setObjectName("line_horizontal")
        # -----------------------Frame_TPRL_results----------------------
        self.frame_tprl_results = QtWidgets.QFrame(self.tab_results)
        self.frame_tprl_results.setGeometry(QtCore.QRect(5, 235, 815, 345))
        self.frame_tprl_results.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tprl_results.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tprl_results.setObjectName('frame_tprl_results')
        # ------------------------Label_Main_TPRL-------------------------
        self.label_main_tprl = QtWidgets.QLabel(self.frame_tprl_results)
        self.label_main_tprl.setGeometry(QtCore.QRect(0, 0, 805, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_main_tprl.setFont(font)
        self.label_main_tprl.setWordWrap(True)
        self.label_main_tprl.setObjectName('label_main_tprl')
        # -----------------------Table_TPRL_results----------------------
        self.table_tprl_results = QtWidgets.QTableWidget(self.frame_tprl_results)
        self.table_tprl_results.setGeometry(QtCore.QRect(0, 45, 805, 260))
        self.table_tprl_results.setContentsMargins(0, 0, 0, 0)
        self.table_tprl_results.setObjectName('table_tprl_results')
        self.table_tprl_results.horizontalHeader().setVisible(False)
        self.table_tprl_results.verticalHeader().setVisible(False)
        # -------------------------Draft_CheckBox-------------------------
        self.check_draft = QtWidgets.QCheckBox(self.frame_tprl_results)
        self.check_draft.setGeometry(QtCore.QRect(435, 310, 180, 30))
        self.check_draft.setObjectName("check_draft")
        self.check_draft.setChecked(False)
        # ----------------------Save_results Button-----------------------
        self.btn_save_results = QtWidgets.QPushButton(self.frame_tprl_results)
        self.btn_save_results.setGeometry(QtCore.QRect(250, 310, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_save_results.setFont(font)
        self.btn_save_results.setObjectName("btn_save_results")

        self.tabWidget.raise_()
        self.labelCalc.raise_()

        self.retranslateUi(AppWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)

    def retranslateUi(self, AppWindow):
        _translate = QtCore.QCoreApplication.translate
        AppWindow.setWindowTitle(_translate("AppWindow", "TPRL Calculator"))
        self.labelCalc.setText(_translate("AppWindow",
                                          "Расчёт уровня зрелости инновационного продукта/технологии к внедрению в ОАО «РЖД»"))
        self.btn_manual.setText(_translate("AppWindow", "Справка"))
        self.btn_change_user.setText(_translate("AppWindow", "Сменить пользователя"))
        # self.btn_change_user1.setText(_translate("AppWindow", "Сменить пользователя"))
        # self.btn_change_user2.setText(_translate("AppWindow", "Сменить пользователя"))
        # self.btn_load_project.setText(_translate("AppWindow", "Загрузить проект"))
        self.btn_new_project.setText(_translate("AppWindow", "Начать новый проект"))
        # self.btn_load_project2.setText(_translate("AppWindow", "Загрузить проект"))
        # self.btn_new_project2.setText(_translate("AppWindow", "Новый проект"))
        self.group_params.setTitle(_translate("AppWindow", "Параметры оценки"))
        self.check_trl.setText(_translate("AppWindow", "Технологическая готовность (TRL)"))
        self.check_mrl.setText(_translate("AppWindow", "Производственная готовность (MRL)"))
        self.check_erl.setText(_translate("AppWindow", "Инженерная готовность (ERL)"))
        self.check_orl.setText(_translate("AppWindow", "Организационная готовность (ORL)"))
        self.check_crl.setText(_translate("AppWindow", "Коммерческая готовность (СRL)"))
        # self.group_types.setTitle(_translate("AppWindow", "Тип проекта"))
        # self.radio_hard.setText(_translate("AppWindow", "Разработка оборудования"))
        # self.radio_soft.setText(_translate("AppWindow", "Разработка программного обеспечения"))
        # self.radio_both.setText(_translate("AppWindow", "Разработка оборудования и ПО"))
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
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user), _translate("AppWindow", "Черновики"))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user2), _translate("AppWindow", "Завершенные"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calc), _translate("AppWindow", "Калькулятор"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_results), _translate("AppWindow", "Результат"))
        self.param_tabs.setTabText(self.param_tabs.indexOf(self.tab_trl_tasks), _translate("AppWindow", "TRL"))
        self.param_tabs.setTabText(self.param_tabs.indexOf(self.tab_mrl_tasks), _translate("AppWindow", "MRL"))
        self.param_tabs.setTabText(self.param_tabs.indexOf(self.tab_erl_tasks), _translate("AppWindow", "ERL"))
        self.param_tabs.setTabText(self.param_tabs.indexOf(self.tab_orl_tasks), _translate("AppWindow", "ORL"))
        self.param_tabs.setTabText(self.param_tabs.indexOf(self.tab_crl_tasks), _translate("AppWindow", "CRL"))
        self.trl_tasks.headerItem().setText(0, _translate("AppWindow", "Параметр"))
        self.trl_tasks.headerItem().setText(1, _translate("AppWindow", "Задачи"))
        self.mrl_tasks.headerItem().setText(0, _translate("AppWindow", "Параметр"))
        self.mrl_tasks.headerItem().setText(1, _translate("AppWindow", "Задачи"))
        self.erl_tasks.headerItem().setText(0, _translate("AppWindow", "Параметр"))
        self.erl_tasks.headerItem().setText(1, _translate("AppWindow", "Задачи"))
        self.orl_tasks.headerItem().setText(0, _translate("AppWindow", "Параметр"))
        self.orl_tasks.headerItem().setText(1, _translate("AppWindow", "Задачи"))
        self.crl_tasks.headerItem().setText(0, _translate("AppWindow", "Параметр"))
        self.crl_tasks.headerItem().setText(1, _translate("AppWindow", "Задачи"))
        self.btn_calculate.setText(_translate("AppWindow", "Рассчитать"))
        self.btn_reset_tasks.setText(_translate("AppWindow", "Сбросить задачи"))
        self.btn_save_results.setText(_translate("AppWindow", "Сохранить"))
        self.enter_project_num.setPlaceholderText(_translate("AppWindow", 'Введите номер проекта...'))
        self.enter_project_date.setPlaceholderText(_translate("AppWindow", 'Введите дату регистрации проекта...'))
        self.enter_theme.setPlaceholderText(_translate("AppWindow", 'Введите тему проекта...'))
        self.enter_initiator.setPlaceholderText(_translate("AppWindow", 'Введите наименование инициатора...'))
        self.enter_customer.setPlaceholderText(_translate("AppWindow", 'Введите наименование заказчика...'))
        self.label_ugt1.setText(_translate("AppWindow", "1"))
        self.label_ugt2.setText(_translate("AppWindow", "2"))
        self.label_ugt3.setText(_translate("AppWindow", "3"))
        self.label_ugt4.setText(_translate("AppWindow", "4"))
        self.label_ugt5.setText(_translate("AppWindow", "5"))
        self.label_ugt6.setText(_translate("AppWindow", "6"))
        self.label_ugt7.setText(_translate("AppWindow", "7"))
        self.label_ugt8.setText(_translate("AppWindow", "8"))
        self.label_ugt9.setText(_translate("AppWindow", "9"))
