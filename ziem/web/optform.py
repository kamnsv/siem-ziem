"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, SelectField, TextAreaField
from wtforms import FormField, validators, BooleanField
from wtforms import DateTimeLocalField, PasswordField
from flask_wtf import FlaskForm
import datetime

                
class OptForm(FlaskForm):
    name = StringField(
        'Название', 
        [validators.DataRequired(),
        validators.Length(min=2, max=50)],
        render_kw={
            'minlength':2,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название параметра'})
    desc = StringField(
        'Описание', 
        [validators.DataRequired(),
        validators.Length(min=3, max=50)],
        render_kw={
            'minlength':3,
            'maxlength':250,
            'class':'form-control', 
            'title':'Описание параметра'})

class BksForm(OptForm):
    api = StringField(
        'Источник', 
        [validators.Optional()],
        render_kw={
            'class':'form-control', 
            'title':'API источник'})
    
    token = PasswordField(
        'Токен', 
        [validators.Optional()],
        render_kw={
            'class':'form-control', 
            'title':'Токен для авторизации'})
    
    updated = DateTimeLocalField(
        'Обновлено',
        [validators.Optional()],
        format='%Y-%m-%dT%H:%M',
        render_kw={
            'readonly': True,
            'class':'form-control'
        })
    
    scheduled = DateTimeLocalField(
        'Запланировано',
        [validators.Optional()],
        format='%Y-%m-%dT%H:%M',
        render_kw={
            'class':'form-control'
        })
    
    data_list_key = StringField(
        'Список', 
        [validators.Optional()],
        render_kw={
            'class':'form-control', 
            'title':'Название ключа со списков теле JSON'})
    
    data_value_key = StringField(
        'Значение', 
        [validators.Optional()],
        render_kw={
            'class':'form-control', 
            'title':'Название ключа значания в списке JSON'})
    
    active = BooleanField('Активное обновление', default=True)
    
class JsonForm(FlaskForm):
    jdata = TextAreaField(
        'Данные в формате JSON', 
        [validators.DataRequired(),
        validators.Length(min=10, max=500000, message="Длина не менее 10 символов")],
        description='Данные')
    backup = SelectField('Бэкап')

class SearchForm(FlaskForm):
    searchInput = StringField(
        'Фильтр', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':''})
    selected_obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        choices=[("main", "Основной")],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Принадлежность источника к объекту'})
