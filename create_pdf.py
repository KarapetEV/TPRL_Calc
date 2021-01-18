from fpdf import FPDF


class CreatePDF:
    def __init__(self, data):
        self.data = data

    def create_file(self):
        date = self.data[0][0]
        project_num = self.data[0][1]
        user = self.data[0][2]
        params = self.data[0][3]
        frame = self.data[1][0]
        print(f"Дата: {date}")
        print(f"№ проекта: {project_num}")
        print(f"Эксперт: {user}")
        print(f"Параметры: {params}")
