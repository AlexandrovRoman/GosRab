import openpyxl
from app import global_init
from users.models import User
from news.models import News, Courses


global_init('app.db')


def export_from_excel(file, add_func):
    wb = openpyxl.load_workbook(filename=file)
    sheet = wb.active
    for i in range(1, sheet.max_row + 1):
        params = [sheet.cell(row=i, column=j).value for j in range(1, sheet.max_column + 1)]
        add_func(*params)


export_from_excel('users.xlsx', User.user_add)
export_from_excel('news.xlsx', News.new)
export_from_excel('courses.xlsx', Courses.new)
