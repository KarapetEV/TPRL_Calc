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
import pandas as pd
from math import ceil
import os


class ReportUgt:

    def __init__(self, data, param_results):
        self.pdf = None
        self.path = ''
        self.data = data
        self.res = {}
        self.results = self.data[0][4]
        self.param_results = param_results
        self.tprl = self.data[0][5][0]
        self.tprl_name = f"Уровень {self.tprl}. {self.data[0][5][1]}"
        self.title = ["Экспертное заключение № ____",
                       "по оценке информации о результатах",
                       "проекта для различных параметров"]
        self.text = ['1.    Дата проведения экспертного оценивания: ',
                     '2.    Идентификационный номер проекта: ',
                     '3.    ФИО эксперта: ',
                     '4.    Тип параметра: ']
        self.table_header = '5.    Статус выполнения оцениваемого уровня и его подуровней '
        self.sign = '6.    Подпись эксперта: ________________________'

    def set_data(self):
        new_data = []
        for i in range(4):
            text = self.data[0][i]
            if i == 3:
                text = ', '.join(self.data[0][i])
            new_data.append(text)

        self.create_pdf(new_data)

    def make_states_dict(self, count):
        d2 = {}
        state = {1: 'Да', 0: 'Нет', -1: 'Не применимо'}
        for k, v in self.param_results.items():
            index = self.res[k]
            l1 = []
            if index > 1 and count == 2:
                for i in range(index - 2, index):
                    l2 = []
                    for el in v[i]:
                        l2.append(state[el])
                    l1.append(l2)
            else:
                l2 = []
                for el in v[index - 1]:
                    l2.append(state[el])
                l1.append(l2)
            d2[k] = l1
        return d2

    def create_pdf(self, data):
        self.res = {}
        self.params = self.data[0][3]
        self.param_float = {}
        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.add_font('times', '', r"fonts/times/times.ttf", uni=True)
        self.pdf.add_page()
        self.pdf.add_font('timesbd', '', r"fonts/times/timesbd.ttf", uni=True)
        self.pdf.set_font("timesbd", size=12)
        for i in range(len(self.title)):
            self.pdf.cell(200, 5, txt=self.title[i], ln=1, align="C")
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        for i in range(4):
            text = self.text[i]
            self.pdf.set_font("times", size=12)
            self.pdf.cell(100, 8, text, '', 0, align="L")
            self.pdf.set_font("times", 'U', size=12)
            self.pdf.cell(80, 8, data[i], '', 0, align="L")
            self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("times", 'U', size=12)
        tprl_name_list = self.word_wrap(self.tprl_name, 95)
        for i in range(len(tprl_name_list)):
            self.pdf.cell(100, 5, tprl_name_list[i].strip(), '', 0, align="L")
            self.pdf.ln()
        if len(tprl_name_list) > 1:
            y = 95
        else:
            y = 90
        if len(self.params) == 5:
            self.pdf.image('chart_pdf.png', 60, y, 84, 50)
            for _ in range(11):
                self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("times", size=12)
        self.pdf.cell(200, 8, txt=self.table_header, align="L")

        for i in range(len(self.params)):
            self.res[self.params[i]] = int(ceil(self.results[i]))
            self.param_float[self.params[i]] = self.results[i]

        for k, v in self.res.items():
            df = self.data[1][k]
            self.create_table(k, v, df)

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

    def remove_pkl(self):
        os.chdir("../../..")
        dir = os.getcwd() + "\\fonts\\times\\"
        files = os.listdir(dir)
        for file in files:
            if file.endswith(".pkl"):
                os.remove(dir + file)

    def get_path(self):
        file_date = self.data[0][0]
        self.project_num = self.data[0][1]
        expert_name = self.data[0][2]
        saved_file_name = self.check_filename(self.project_num)
        new_file_name = self.check_filename(f'{saved_file_name}_{file_date}.pdf')
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

    def create_table(self, param, lvl, df):

        self.pdf.ln()
        self.pdf.set_font("times", 'U', size=12)
        self.pdf.cell(200, 5, txt=f"Установленный уровень готовности параметра "
                                  f"{param} - {self.param_float[param]}", ln=1, align="L")
        self.pdf.ln()

        count = 0
        if lvl > 1 and float(lvl) != self.param_float[param]:
            count = 2
            lvl -= 1
        else:
            count = 1
        param_states = self.make_states_dict(count)[param]
        if lvl != 0:
            self.pdf.set_font("timesbd", size=10)
            self.pdf.cell(20, 5, 'Уровень', 1, 0, align="C")
            self.pdf.cell(140, 5, 'Наименование задачи', 1, 0, align="C")
            self.pdf.cell(30, 5, 'Статус', 1, 0, align="C")
            self.pdf.ln()
            self.pdf.set_font("times", size=10)

            for i in range(count):
                states = param_states[i]

                levels = df.loc[df['Level'] == (lvl + i)]
                level = levels.iat[0, 0]
                lvls = levels.iat[0, 1]
                level_name_list = self.word_wrap(lvls, 95)
                level_count = levels.shape[0]
                tasks = levels['Task'].tolist()
                level_num_list = self.make_line_list(f'Уровень {level}', len(level_name_list))
                for lvl_line in range(len(level_name_list)):
                    level_num = level_num_list[lvl_line]
                    level_name = level_name_list[lvl_line]
                    border_num = 'L'
                    border_lvl = 'R'
                    if lvl_line == 0:
                        border_num = 'LT'
                        border_lvl = 'TR'
                    elif lvl_line == len(level_name_list) - 1:
                        border_num = 'LB'
                        border_lvl = 'RB'
                    if len(level_name_list) == 1:
                        border_num = 'LTB'
                        border_lvl = 'TRB'
                        level_num = f'Уровень {level}'
                        level_name = lvls
                    self.pdf.set_font("times", 'U', size=10)
                    self.pdf.cell(20, 5, level_num, border_num, 0, align="L")
                    self.pdf.set_font("times", size=10)
                    self.pdf.cell(170, 5, level_name, border_lvl, 0, align="L")
                    self.pdf.ln()
                for j in range(level_count):
                    task_list = self.word_wrap(f'{tasks[j]}', 80)
                    num_list = self.make_line_list(f'№ {j + 1}', len(task_list))
                    states_list = self.make_line_list(states[j], len(task_list))
                    for k in range(len(task_list)):
                        num = num_list[k]
                        task = task_list[k]
                        state = states_list[k]
                        border = 'LR'
                        if k == 0:
                            border = 'LTR'
                        elif k == len(task_list) - 1:
                            border = 'LRB'
                        if len(task_list) == 1:
                            border = 1
                            num = f'№ {j + 1}'
                            task = f'{tasks[j]}'
                            state = states[j]
                        self.pdf.cell(20, 5, num, border, 0, align="C")
                        self.pdf.cell(140, 5, task, border, 0, align="L")
                        self.pdf.cell(30, 5, state, border, 0, align="C")
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
            result = line
        return result
