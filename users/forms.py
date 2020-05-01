from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, AnyOf, EqualTo
from wtforms.fields import SelectField


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    fathername = StringField('Отчество', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[("Мужской", "Мужской"), ("Женский", "Женский")],
                      validators=[DataRequired(), AnyOf(['Женский', 'Мужской'])])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    email = EmailField('Почта', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class EditForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    fathername = StringField('Очество', validators=[DataRequired()])
    sex = SelectField('Пол', choices=[("Мужской", "Мужской"), ("Женский", "Женский")], validators=[DataRequired()])
    marriage = SelectField('Семейное положение', choices=[("В браке", "В браке"), ("Не в браке", "Не в браке")])
    email = EmailField('Почта', validators=[Email()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    about_myself = StringField('Информация о себе', validators=[DataRequired()])
    submit = SubmitField('Редактировать')


class SignInForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()],
                       render_kw={"placeholder": "Адрес электронной почты"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')


class ForgotPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Пароль повторно', validators=[EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Сменить')


class RestorePasswordForm(FlaskForm):
    email = EmailField('Ваш email', validators=[DataRequired()])
    submit = SubmitField('Прислать письмо')
