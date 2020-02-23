import openpyxl
from app import global_init
from users.views import user_add


def export_users_from_excel(file='excel_example.xlsx'):
    global_init('app.db')
    wb = openpyxl.load_workbook(filename=file)
    sheet = wb.active
    for i in range(1, sheet.max_row + 1):
        user_params = [sheet.cell(row=i, column=j).value for j in range(1, sheet.max_column + 1)]
        user_add(*user_params)

export_users_from_excel()
