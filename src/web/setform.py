"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, TextAreaField, SelectField
from wtforms import FormField, validators
from flask_wtf import FlaskForm
from wtforms.fields import DateField, TimeField, DateTimeLocalField

class SettingForm(FlaskForm):
    cor_name = StringField(
        'Название коррелятора', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название коррелятора, привязанное к площадке: TVV_SIKN432'})
    repo_ip = StringField(
        'IP адрес', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':15,
            'class':'form-control', 
            'title':'Адрес сервера обновлений'})
    repo_port = StringField(
        'PORT', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':5,
            'class':'form-control', 
            'title':'Порт сервера обновлений'})
    sender_ip = StringField(
        'IP адрес сендера', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':15,
            'class':'form-control', 
            'title':'Адрес сендера, куда отправлять данные'})
    sender_port = StringField(
        'PORT сендера', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':5,
            'class':'form-control', 
            'title':'Порт сендера, куда отправлять данные'})
    opc_ip = StringField(
        'IP адрес OPC сервера', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':15,
            'class':'form-control', 
            'title':'Адрес OPC сервера, куда отправлять данные'})
    opc_port = StringField(
        'PORT OPC сервера', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':5,
            'class':'form-control', 
            'title':'Порт OPC сервера, куда отправлять данные'})

class JsonForm(FlaskForm):
    jdata = TextAreaField(
        'Данные в формате JSON', 
        [validators.DataRequired(),
        validators.Length(min=10, max=5000000, message="Длина не менее 10 символов")],
        description='Данные')
    backup = SelectField('Бэкап')

class SearchForm(FlaskForm):
    searchInput = StringField(
        'Фильтр', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'123123'})
    meta_field = StringField(
        'Источник', 
        [validators.DataRequired()],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':''})
    date_start = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(format='%Y-%m-%dT%H:%M')

class MapsearchForm(FlaskForm):
    search = StringField(
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Поиск',
        render_kw={"placeholder": "Поиск"})
    date_start = DateField()
    time_start = TimeField()
    date_end = DateField()
    time_end = TimeField()
