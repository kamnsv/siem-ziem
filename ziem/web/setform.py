"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
        Kamnev  Sergey
"""

from wtforms import StringField, TextAreaField, SelectField, RadioField
from wtforms import FormField, validators, BooleanField, FieldList
from flask_wtf import FlaskForm
from wtforms.fields import DateField, TimeField, DateTimeLocalField

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


class ColsForm(FlaskForm):
    class Meta:
        csrf = False
        
    on = BooleanField('Активная передача', default=True)
    
    url = StringField(
        'Адрес', 
        [validators.Length(max=5000)],
        render_kw={
            'maxlength':5000,
            'title':'URL-адрес API или иной параметр передачи'})

class SenderForm(FlaskForm):
    class Meta:
        csrf = False
    
    name = StringField(
        'Название', 
        [validators.Length(max=5000)],
        render_kw={
            'maxlength':5000,
            'title':'Название журнала для сбора при активном подключении'})
    
    prot = RadioField('Протокол передачи', 
                      choices=[('http','HTTP'),
                               ('opcua','OPCUA'),
                               ('systcp','Syslog TCP'),
                               ('sysudp','Syslog UDP'),])
    
    ip = StringField(
        'IP адрес', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':15,
            'class':'form-control', 
            'title':'IP-aдреc'})
    
    port = StringField(
        'PORT', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':5,
            'class':'form-control', 
            'title':'Порт'})
    
    enabled = BooleanField('Активная отправка', default=True)
    
    alrs = FormField(ColsForm)
    eves = FormField(ColsForm)
    incs = FormField(ColsForm)
    
class SettingForm(FlaskForm):
    
    senders = FieldList(FormField(SenderForm), min_entries=1)
