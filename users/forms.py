from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    email = EmailField('Ваш email', validators=[DataRequired()], render_kw={"placeholder": "Электронная почта"})
    submit = SubmitField('Прислать письмо')


class NotificationForm(FlaskForm):
    access_desire_for_work_owner = BooleanField('Предоставить доступ работадателям просматривать ваше желание.')
    access_desire_for_personnel = BooleanField('Предоставить доступ кадровикам просматривать ваше желание.')
    access_redaction_for_work_owner = BooleanField('Предоставить доступ работадателю вносить изменения в ваш профиль.')
    access_redaction_for_personnel = BooleanField('Предоставить доступ кадровикам вносить изменения в ваш профиль.')

    notify_vacancy = BooleanField('Получать уведомления, о новых подходящих вакансиях.')
    notify_cources = BooleanField('Получать уведомления, о новых курсах, которые могут вам понравится.')
    notify_redaction = BooleanField('Получать уведомления, о изменениях профиля кадровиками, или работадателем.')
    notify_projects = BooleanField('Получать уведомления, о проектой деятельности.')
    notify_public_activities = BooleanField('Получать уведомления, о ообщественной деятельности.')

    submit = SubmitField('Применить')
