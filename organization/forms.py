from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, AnyOf


class AddOrganizationForm(FlaskForm):
    name = StringField('Имя организации', validators=[DataRequired()])
    org_type = SelectField('Вид организации', choices=[("ООО", "ООО"), ("АО", "АО"), ("ИП", "ИП")],
                           validators=[DataRequired(), AnyOf(['ООО', 'АО', 'ИП'])])
    email = EmailField('Почта организации', validators=[Email()])
    org_desc = TextAreaField('Описание организации')
    submit = SubmitField('Добавить организацию')


class SendResumeForm(FlaskForm):
    content = TextAreaField('Ваше резюме')
    submit = SubmitField('Оправить работодателю')
