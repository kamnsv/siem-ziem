"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, SelectField, TextAreaField
from wtforms import FormField, validators
from flask_wtf import FlaskForm

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
            'maxlength':50,
            'class':'form-control', 
            'title':'Описание параметра'})

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
