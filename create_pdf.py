from fpdf import FPDF
import pandas as pd
from math import ceil
import os



class CreatePDF:

    def __init__(self, data, param_results):
        self.pdf = None
        self.path = ''
        self.data = data
        self.res = {}
        self.results = self.data[0][4]
        self.param_results = param_results
        self.header = ["Экспертное заключение",
                      "по оценке информации о результатах",
                      "инновационного проекта в области железнодорожного транспорта"]
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

    def make_states_dict(self):
        d2 = {}
        state = {1: 'Да', 0: 'Нет', -1: 'Не применимо'}
        for k, v in self.param_results.items():
            index = self.res[k]
            l1 = []
            if index > 1:
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
        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.add_font('times', '', r"fonts/times/times.ttf", uni=True)
        self.pdf.add_page()
        self.pdf.add_font('timesbd', '', r"fonts/times/timesbd.ttf", uni=True)
        self.pdf.set_font("timesbd", size=12)
        for i in range(len(self.header)):
            self.pdf.cell(200, 5, txt=self.header[i], ln=1, align="C")
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
        self.pdf.set_font("times", size=12)
        self.pdf.cell(200, 8, txt=self.table_header, ln=1, align="L")
        params = self.data[0][3]

        for i in range(len(params)):
            self.res[params[i]] = int(ceil(self.results[i]))

        for k, v in self.res.items():
            self.create_table(k, v)

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.set_font("times", size=12)
        self.pdf.cell(200, 8, txt=self.sign, ln=1, align="L")
        file_path = self.get_path()[0] + self.get_path()[1]
        self.pdf.output(file_path, "F")
        os.chdir(self.get_path()[0])
        open_path = os.getcwd() + f"\\{self.get_path()[1]}"
        os.startfile(open_path)
        self.remove_pkl()

    def remove_pkl(self):
        os.chdir("../../..")
        dir = os.getcwd() + "\\fonts\\times\\"
        files = os.listdir(dir)
        for file in files:
            if file.endswith(".pkl"):
                os.remove(dir+file)

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

    def create_table(self, param, lvl):
        df = pd.read_excel("Param_Tasks.xlsx", sheet_name=param)
        param_states = self.make_states_dict()[param]
        count = 0
        if lvl > 1:
            count = 2
            lvl -= 1
        else:
            count = 1

        self.pdf.ln()
        self.pdf.set_font("times", 'U', size=12)
        self.pdf.cell(190, 5, txt=param, ln=1, align="L")
        self.pdf.ln()
        self.pdf.set_font("times", size=10)
        self.pdf.cell(20, 5, 'Уровень', 1, 0, align="C")
        self.pdf.cell(140, 5, 'Наименование задачи', 1, 0, align="C")
        self.pdf.cell(30, 5, 'Статус', 1, 0, align="C")
        self.pdf.ln()

        for i in range(count):
            states_list = param_states[i]

            levels = df.loc[df['Level'] == (lvl+i)]
            level = levels.iat[0, 0]
            level_name = levels.iat[0, 1]
            level_count = levels.shape[0]
            tasks = levels['Task'].tolist()

            level_text1 = level_name[:90]
            level_text2 = level_name[90:180]
            level_text3 = level_name[180:]

            self.pdf.set_font("times", 'U', size=10)
            self.pdf.cell(20, 5, f'Уровень {level}', 'LT', 0, align="L")
            self.pdf.set_font("times", size=10)
            self.pdf.cell(170, 5, level_text1, 'TR', 0, align="L")
            self.pdf.ln()
            self.pdf.cell(20, 5, '', 'L', 0, align="L")
            self.pdf.cell(170, 5, level_text2, 'R', 0, align="L")
            self.pdf.ln()
            self.pdf.cell(20, 5, '', 'LB', 0, align="L")
            self.pdf.cell(170, 5, level_text3, 'RB', 0, align="L")
            self.pdf.ln()
            for j in range(level_count):
                task = f'{tasks[j]}'
                task1 = task[:80]
                task2 = task[80:160]
                task3 = task[160:]
                self.pdf.cell(20, 5, f'№ {j + 1}', 'LTR', 0, align="C")
                self.pdf.cell(140, 5, task1, 'LTR', 0, align="L")
                self.pdf.cell(30, 5, states_list[j], 'LTR', 0, align="C")
                self.pdf.ln()
                self.pdf.cell(20, 5, '', 'LR', 0, align="C")
                self.pdf.cell(140, 5, task2, 'LR', 0, align="L")
                self.pdf.cell(30, 5, '', 'LR', 0, align="C")
                self.pdf.ln()
                self.pdf.cell(20, 5, '', 'LRB', 0, align="C")
                self.pdf.cell(140, 5, task3, 'LRB', 0, align="L")
                self.pdf.cell(30, 5, '', 'LRB', 0, align="C")
                self.pdf.ln()