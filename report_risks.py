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


class ReportRisks:
    def __init__(self, data, table):
        self.pdf = None
        self.data = data
        self.table = table
        self.title = ["Экспертное заключение № ____",
                       "по оценке рисков реализации и финансирования",
                       "инновационных проектов в ОАО «РЖД»"]
        self.text = ['1.    Дата проведения экспертного оценивания: ',
                     '2.    Идентификационный номер проекта: ',
                     '3.    ФИО эксперта: ',
                     ]
        self.table_title = '4.    Оценка рисков по проекту:'
        self.sign = '5.    Подпись эксперта: ________________________'
        self.create_pdf()

    def create_pdf(self):
        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.add_font('times', '', r"fonts/times/times.ttf", uni=True)
        self.pdf.add_font('timesbd', '', r"fonts/times/timesbd.ttf", uni=True)
        self.pdf.add_page()

        self.pdf.set_font("timesbd", size=12)
        for i in range(len(self.title)):
            self.pdf.cell(200, 5, txt=self.title[i], ln=1, align="C")

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()

        for i in range(len(self.text)):
            text = self.text[i]
            self.pdf.set_font("times", size=12)
            self.pdf.cell(100, 8, text, '', 0, align="L")
            self.pdf.set_font("times", 'U', size=12)
            self.pdf.cell(80, 8, self.data[i], '', 0, align="L")
            self.pdf.ln()

        self.pdf.set_font("times", size=12)
        self.pdf.cell(100, 8, self.table_title, '', 0, align="L")

        self.create_table()

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("times", size=12)
        self.pdf.cell(200, 8, txt=self.sign, ln=1, align="L")

        path_list = self.get_path()
        file_path = path_list[0] + path_list[1]
        self.pdf.output(file_path, "F")
        os.chdir(path_list[0])
        open_path = os.getcwd() + f"\\{path_list[1]}"
        os.startfile(open_path)
        self.remove_pkl()

    def create_table(self):
        table_headers = []
        columns = self.table.columnCount()
        for i in range(columns):
            table_headers.append(self.table.horizontalHeaderItem(i).text())

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("timesbd", size=10)
        self.pdf.cell(30, 5, table_headers[0], 1, 0, align="C")
        self.pdf.cell(135, 5, table_headers[1], 1, 0, align="C")
        self.pdf.cell(25, 5, table_headers[2], 1, 0, align="C")
        self.pdf.ln()

        self.pdf.set_font("times", size=10)
        rows = self.table.rowCount()
        for i in range(rows):
            risk_group = self.word_wrap(self.table.cellWidget(i, 0).text(), 20)
            risk_name = self.word_wrap(self.table.cellWidget(i, 1).text(), 80)
            risk_num = self.table.cellWidget(i, 2).text()
            border_left = 'LB'
            border_right = 'RB'
            border = 'LRB'
            count = 1
            if 1 <= len(risk_group) <= len(risk_name):
                count = len(risk_name)
                if len(risk_group) == 1:
                    risk_group = self.make_line_list(self.table.cellWidget(i, 0).text(), count)
                risk_num = self.make_line_list(self.table.cellWidget(i, 2).text(), count)
            elif 1 <= len(risk_name) <= len(risk_group):
                count = len(risk_group)
                if len(risk_name) == 1:
                    risk_name = self.make_line_list(self.table.cellWidget(i, 1).text(), count)
                risk_num = self.make_line_list(self.table.cellWidget(i, 2).text(), count)
            if count > 1:
                border_left = 'L'
                border_right = 'R'
                border = 'LR'
            for j in range(count):
                if j == count - 1:
                    border_left = 'LB'
                    border_right = 'RB'
                    border = 'LRB'
                self.pdf.cell(30, 5, risk_group[j], border_left, 0, align="C")
                self.pdf.cell(135, 5, risk_name[j], border, 0, align="L")
                self.pdf.cell(25, 5, risk_num[j], border_right, 0, align="C")
                self.pdf.ln()

    def word_wrap(self, line, x):
        if '\n' in line:
            line = line.replace('\n', ' ')
        start = 0
        l1 = []
        if len(line) > x:
            while len(line) > (start + x):
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
        os.chdir("../../..")
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

