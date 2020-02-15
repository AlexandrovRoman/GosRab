from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Optional


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    fathername = StringField('Очество', default='', validators=[Optional()])
    sex = StringField('Пол (М, Ж)', validators=[DataRequired()])
    start_place = StringField('Место рождения',  validators=[DataRequired()])
    nationality = StringField('Гражданство',  validators=[DataRequired()])
    education = StringField('Образование', default='', validators=[Optional()])
    date_of_birth = DateTimeLocalField('Дата рождения', format='%d/%m/%y', validators=[DataRequired()])
    marriage = BooleanField('В браке', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Получать уведомления о событиях')
    submit = SubmitField('Войти')
