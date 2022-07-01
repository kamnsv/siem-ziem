"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms import validators, PasswordField
from flask_wtf import FlaskForm

class RuleForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название объекта'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание правила'})
    sender_ip = StringField(
        'IP адрес Sender', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Адрес сендера'})
    updateagent = BooleanField('Обновить Агента', default=False)
    restartziem = BooleanField('Перезапустить ZIEM', default=False)
    updateziem = BooleanField('Обновить ZIEM', default=False)
    updateconfig = BooleanField('Обновить Конфигурацию', default=False)
    version_agent = StringField('Версия Агента', render_kw={'readonly': True})
    version_ziem = StringField('Версия ZIEM', render_kw={'readonly': True})
    pswd = PasswordField(
        'Пароль *', 
        [validators.Optional(), 
        validators.Length(min=10, max=25)],
        description='Пароль',
        render_kw={
            'minlength':10,
            'maxlength':25,
            'class':'form-control', 
            'title':'Одноразовый пароль при подключении агента'})

class SearchForm(FlaskForm):
    searchInput = StringField(
        'Фильтр', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':''})
    
class JsonForm(FlaskForm):
    jdata = TextAreaField(
        'Данные в формате JSON', 
        [validators.DataRequired(),
        validators.Length(min=10, max=5000000, message="Длина не менее 10 символов")],
        description='Данные')
    backup = SelectField('Бэкап')