from fpdf import FPDF
import pandas as pd
from math import ceil


class CreatePDF:
    def __init__(self, data, results, param_results):
        self.pdf = None
        self.data = data
        self.results = results
        self.param_results = param_results
        self.header = ["Экспертное заключение",
                      "по оценке информации о результатах",
                      "инновационного проекта в области железнодорожного транспорта"]
        self.text = ['1.    Дата проведения экспертного оценивания: ',
                     '2.    Идентификационный номер проекта: ',
                     '3.    ФИО эксперта: ',
                     '4.    Тип параметра: ']
        self.table_header = '5.    Статус выполнения оцениваемого уровня и его подуровней '
        self.sign = '6.    Подпись эксперта: _____________________'

    def set_data(self):
        new_data = []
        for i in range(4):
            text = self.data[0][i]
            if i == 3:
                text = ', '.join(self.data[0][i])
            new_data.append(text)

        self.create_pdf(new_data)

    def create_pdf(self, data):
        res = {}
        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.add_page()
        self.pdf.add_font('timesbd', '', r"c:\mypython\test\fonts\times\timesbd.ttf", uni=True)
        self.pdf.set_font("timesbd", size=12)
        for i in range(len(self.header)):
            self.pdf.cell(200, 5, txt=self.header[i], ln=1, align="C")
        self.pdf.ln()
        self.pdf.ln()
        self.pdf.ln()
        for i in range(4):
            text = self.text[i] + data[i]
            self.pdf.add_font('times', '', r"c:\mypython\test\fonts\times\times.ttf", uni=True)
            self.pdf.set_font("times", size=12)
            self.pdf.cell(200, 8, txt=text, ln=1, align="L")
        self.pdf.cell(200, 8, txt=self.table_header, ln=1, align="L")
        params = self.data[0][3]

        for i in range(len(params)):
            res[params[i]] = int(ceil(self.results[i]))

        for k, v in res.items():
            self.create_table(k, v)

        self.pdf.ln()
        self.pdf.ln()
        self.pdf.cell(200, 8, txt=self.sign, ln=1, align="L")

        self.pdf.output("demo.pdf", "F")

    def create_table(self, param, lvl):
        df = pd.read_excel("Param_Tasks.xlsx", sheet_name=param)

        count = 0
        if lvl > 1:
            count = 2
            lvl -= 1
        else:
            count = 1
        self.pdf.ln()
        self.pdf.cell(190, 5, txt=param, ln=1, align="L")
        self.pdf.ln()
        self.pdf.cell(30, 5, 'Уровень', 1, 0, align="C")
        self.pdf.cell(130, 5, 'Наименование задачи', 1, 0, align="C")
        self.pdf.cell(30, 5, 'Статус', 1, 0, align="C")
        self.pdf.ln()

        for i in range(count):
            levels = df.loc[df['Level'] == (lvl+i)]
            level = levels.iat[0, 0]
            level_name = levels.iat[0, 1]
            level_count = levels.shape[0]
            tasks = levels['Task'].tolist()
            level_text = f'Уровень {level}: {level_name}'
            level_text1 = level_text[:80]
            level_text2 = level_text[80:160]
            level_text3 = level_text[160:]
            self.pdf.cell(190, 5, level_text1, 'LTR', 0, align="L")
            self.pdf.ln()
            self.pdf.cell(190, 5, level_text2, 'LR', 0, align="L")
            self.pdf.ln()
            self.pdf.cell(190, 5, level_text3, 'LRB', 0, align="L")
            self.pdf.ln()
            for j in range(level_count):
                task = f'{tasks[j]}'
                task1 = task[:50]
                task2 = task[50:100]
                task3 = task[100:]
                self.pdf.cell(30, 5, f'№ {j + 1}', 'LTR', 0, align="C")
                self.pdf.cell(130, 5, task1, 'LTR', 0, align="L")
                self.pdf.cell(30, 5, 'Да', 'LTR', 0, align="C")
                self.pdf.ln()
                self.pdf.cell(30, 5, '', 'LR', 0, align="C")
                self.pdf.cell(130, 5, task2, 'LR', 0, align="L")
                self.pdf.cell(30, 5, '', 'LR', 0, align="C")
                self.pdf.ln()
                self.pdf.cell(30, 5, '', 'LRB', 0, align="C")
                self.pdf.cell(130, 5, task3, 'LRB', 0, align="L")
                self.pdf.cell(30, 5, '', 'LRB', 0, align="C")
                self.pdf.ln()