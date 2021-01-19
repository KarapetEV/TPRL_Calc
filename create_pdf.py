from fpdf import FPDF
import pandas as pd
from math import ceil


class CreatePDF:
    def __init__(self, data, results):
        self.pdf = None
        self.data = data
        self.results = results
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
        # date = self.data[0][0]
        # project_num = self.data[0][1]
        # user = self.data[0][2]
        # params = self.data[0][3]
        # frame = self.data[1][0]
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

        for param in params:
            for result in self.results:
                res[param] = ceil(result)

        for k, v in res.items():
            self.create_table(k, v)

        self.pdf.cell(200, 8, txt=self.sign, ln=1, align="L")

        self.pdf.output("demo.pdf", "F")

    def create_table(self, param, lvl):
        df = pd.read_excel("Param_Tasks.xlsx", sheet_name=param)
        level_min = df.loc[df['Level'] == (lvl - 1)]
        level_max = df.loc[df['Level'] == (lvl)]
        level_min_name = level_min.iat[0, 1]
        level_max_name = level_max.iat[0, 1]
        level_min_count = level_min.shape[0]
        level_max_count = level_max.shape[0]
        tasks_min = level_min['Task'].tolist()
        tasks_max = level_max['Task'].tolist()

        self.pdf.ln()
        self.pdf.cell(40, 5, 'Уровень/задача', 1, 0, align="C")
        self.pdf.cell(120, 5, 'Наименование задачи', 1, 0, align="C")
        self.pdf.cell(40, 5, 'Статус', 1, 0, align="C")
        self.pdf.cell(200, 5, f'Уровень {level_min}: {level_min_name}', 1, 0, align="L")
        for i in range(level_min_count):
            self.pdf.cell(40, 5, f'№ {i+1}', 1, 0, align="C")
            self.pdf.cell(120, 5, f'{tasks_min[i]}', 1, 0, align="L")
            self.pdf.cell(40, 5, 'Да', 1, 0, align="C")
        self.pdf.cell(200, 5, f'Уровень {level_max}: {level_max_name}', 1, 0, align="L")
        for i in range(level_max_count):
            self.pdf.cell(40, 5, f'№ {i+1}', 1, 0, align="C")
            self.pdf.cell(120, 5, f'{tasks_max[i]}', 1, 0, align="L")
            self.pdf.cell(40, 5, 'Да', 1, 0, align="C")

