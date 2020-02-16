from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    fathername = StringField('Очество', default='')
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = StringField('Пол (М, Ж)', validators=[DataRequired()])
    start_place = StringField('Место рождения',  validators=[DataRequired()])
    nationality = StringField('Гражданство',  validators=[DataRequired()])
    education = StringField('Образование', default='Отсутствует')
    date_of_birth = DateTimeLocalField('Дата рождения', format='%d/%m/%y', validators=[DataRequired()])
    marriage = BooleanField('В браке', validators=[DataRequired()])
    email = EmailField('', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Получать уведомления о событиях')
    submit = SubmitField('Войти')
