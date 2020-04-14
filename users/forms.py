from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    fathername = StringField('Очество', default='')
    sex = StringField('Пол', validators=[DataRequired()])
    date_of_birth = DateField('Дата рождения', format='%y/%m/%d', validators=[DataRequired()])
    email = EmailField('', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
