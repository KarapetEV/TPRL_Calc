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

from fpdf import FPDF
import os

file_count = 1

class ReportRisks:
    def __init__(self, data, tab, tprl_risk_list):
        self.pdf = None
        self.data = data
        self.tab = tab
        self.tprl_risk_list = tprl_risk_list
        self.title = ["Экспертное заключение № ____",
                       "по оценке рисков реализации и финансирования",
                       "инновационных проектов в ОАО «РЖД»"]
        self.text = ['1.    Дата проведения экспертного оценивания: ',
                     '2.    Идентификационный номер проекта: ',
                     '3.    ФИО эксперта: ',
                     '4.    Тип параметра: '
                     ]
        self.table_title = '5.    Оценка рисков уровней готовности по параметрам:'
        self.final_tprl_risk_text = '6.    Итоговая оценка риска достижения заданного уровня зрелости ' \
                                    'продукта/технологии по совокупности всех параметров'
        self.sign = '7.    Подпись эксперта: ________________________'

        self.data.append(self.get_tab_names())
        self.create_pdf()

    def create_pdf(self):
        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.add_font('times', '', r"fonts/times/times.ttf", uni=True)
        self.pdf.add_font('timesbd', '', r"fonts/times/timesbd.ttf", uni=True)
        self.pdf.add_page()

        self.pdf.set_font("timesbd", size=13)
        for i in range(len(self.title)):
            self.pdf.cell(200, 5, txt=self.title[i], ln=1, align="C")

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()

        for i in range(len(self.text)):
            text = self.text[i]
            self.pdf.set_font("times", size=13)
            self.pdf.cell(100, 8, text, '', 0, align="L")
            self.pdf.set_font("times", 'U', size=13)
            self.pdf.cell(80, 8, self.data[i], '', 0, align="L")
            self.pdf.ln()

        self.pdf.set_font("times", size=13)
        self.pdf.cell(100, 8, self.table_title, '', 0, align="L")
        self.pdf.ln()

        self.create_table()

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("times", size=13)
        self.pdf.cell(200, 8, txt=self.sign, ln=1, align="L")

        path_list = self.get_path()
        file_path = path_list[0] + path_list[1]

        self.save_report(file_path)

        self.remove_pkl()

    def save_report(self, path):
        global file_count

        file = os.path.basename(path)
        file_name = os.path.splitext(file)[0]
        try:
            self.pdf.output(path, "F")
            file_count = 1
        except PermissionError:
            new_file = f"{file_name} ({file_count})"
            file_count += 1
            path = path.replace(file_name, new_file)
            self.pdf.output(path, "F")
        finally:
            open_path = os.path.normpath(os.getcwd() + f"/{path}")
            os.startfile(open_path)

    def get_tab_names(self):
        tabs = []
        tabs_count = self.tab.count()
        for i in range(tabs_count):
            self.tab.setCurrentIndex(i)
            tab = self.tab.tabText(self.tab.currentIndex())
            tabs.append(tab)
        result = ", ".join(tabs)
        return result

    def create_table(self):
        risks_table_headers = ["Задача",
                               "Прогноз своевременного исполнения задачи",
                               "Вероятность реализации риска, %"]
        count = self.tab.count()
        for i in range(count):
            self.tab.setCurrentIndex(i)
            tab = self.tab.currentWidget()
            frame = tab.children()[0]
            widgets = frame.children()
            result_param_risk = widgets[2].text()
            self.pdf.ln()
            self.pdf.set_font("timesbd", 'U', size=13)
            self.pdf.cell(200, 5, txt=result_param_risk, ln=1, align="L")
            param_lvl = widgets[0].text()
            param_lvl.replace("\n", " ")
            param_lvl = self.word_wrap(param_lvl, 100)
            self.pdf.ln()
            self.pdf.set_font("times", size=12)
            for j in range(len(param_lvl)):
                self.pdf.cell(200, 5, txt=param_lvl[j], ln=1, align="C")
            task_head = self.make_line_list(risks_table_headers[0], 3)
            forecast_head = self.word_wrap(risks_table_headers[1], 20)
            risk_realization_head = self.word_wrap(risks_table_headers[2], 15)
            for i in range(3):
                if i == 0:
                    border_left = 'LT'
                    border_right = 'TR'
                    border = 'LTR'
                elif i == 1:
                    border_left = 'L'
                    border_right = 'R'
                    border = 'LR'
                else:
                    border_left = 'LB'
                    border_right = 'RB'
                    border = 'LRB'
                self.pdf.cell(135, 5, task_head[i], border_left, 0, align="C")
                self.pdf.cell(35, 5, forecast_head[i], border, 0, align="C")
                self.pdf.cell(25, 5, risk_realization_head[i], border_right, 0, align="C")
                self.pdf.ln()
            table = widgets[1]
            rows = table.rowCount()
            self.pdf.set_font("times", size=11)
            for row in range(rows):
                task = self.word_wrap(table.item(row, 0).text(), 70)
                count = len(task)
                # forecast_line = ""
                try:
                    forecast_line = table.item(row, 1).text()
                except AttributeError:
                    forecast_line = table.cellWidget(row, 1).text()
                forecast = self.make_line_list(forecast_line, count)
                risk_realization = []
                if row == 0:
                    risk_realization = self.make_line_list(table.item(0, 2).text(), count)
                else:
                    risk_realization = self.make_line_list("", count)
                for i in range(count):
                    border_right = 'R'
                    if i == (count - 1):
                        border_left = 'LB'
                        border = 'LRB'
                        if row == (rows - 1):
                            border_right = 'RB'
                    else:
                        border_left = 'L'
                        border_right = 'R'
                        border = 'LR'
                    self.pdf.cell(135, 5, task[i], border_left, 0, align="L")
                    self.pdf.cell(35, 5, forecast[i], border, 0, align="C")
                    self.pdf.cell(25, 5, risk_realization[i], border_right, 0, align="C")
                    self.pdf.ln()
            self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        self.set_final_tprl_risk_text(count)

    def set_final_tprl_risk_text(self, count):
        self.pdf.set_font("times", size=13)
        if len(self.tprl_risk_list) > 0:
            risk_text = f"{self.final_tprl_risk_text}: {self.tprl_risk_list[0]} - {self.tprl_risk_list[1]}."
            text_list = [risk_text, self.tprl_risk_list[2]]
            for i in range(2):
                self.pdf.multi_cell(200, 5, text_list[i], 0, align="L")
        else:
            text = f"{self.final_tprl_risk_text} не рассчитана."
            self.pdf.multi_cell(200, 5, text, 0, align="L")

    def word_wrap(self, line, x):
        if '\n' in line:
            line = line.replace('\n', ' ')
        start = 0
        l1 = []
        if len(line) >= x:
            while len(line) >= (start + x):
                index = line.rfind(' ', start, start + x)
                res = line[start:index]
                l1.append(res.strip())
                start = index
            l1.append(line[start:].strip())
        else:
            l1.append(line)
        return l1

    def make_line_list(self, line, count):
        result = []
        if count > 1:
            for i in range(count):
                result.append(line)
                line = ''
        else:
            result.append(line)
        return result

    def remove_pkl(self):
        # os.chdir("../../..")
        dir = os.getcwd() + "\\fonts\\times\\"
        files = os.listdir(dir)
        for file in files:
            if file.endswith(".pkl"):
                os.remove(dir + file)

    def get_path(self):
        file_date = self.data[0]
        project_num = self.data[1]
        expert_name = self.data[2]
        saved_file_name = self.check_filename(project_num)
        new_file_name = self.check_filename(f'{saved_file_name}_risks_{file_date}.pdf')
        if not os.path.isdir("Reports"):
            os.mkdir("Reports")
        if not os.path.isdir(f"Reports/{expert_name}"):
            os.mkdir(f"Reports/{expert_name}")
        if not os.path.isdir(f"Reports/{expert_name}/{saved_file_name}"):
            os.mkdir(f"Reports/{expert_name}/{saved_file_name}")
        self.path = f"Reports/{expert_name}/{saved_file_name}/"

        return [self.path, new_file_name]

    def check_filename(self, line):
        chars = ':\/*?<>"|'
        for ch in chars:
            if ch in line:
                line = line.replace(ch, '_')
        return line

