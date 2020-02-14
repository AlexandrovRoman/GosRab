from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    tags = StringField('Тэги через запятую', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')

