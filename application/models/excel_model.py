# -*- coding: utf-8 -*-
from openpyxl import Workbook


class ExcelModel:
    """Generate Excel file and send it to front end.
    """

    def __init__(self, form):
        self.__wb = Workbook()
        self.__ws = self.__wb.create_sheet(form['title'], 0)

    def generate_excel(self):
        pass
