"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, SelectField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms.fields import DateField, TimeField, DateTimeLocalField
from datetime import datetime
from datetime import timedelta

#from wtforms import DateField

class IncForm(FlaskForm):
    search = StringField(
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Поиск',
        render_kw={"placeholder": "Поиск"})
    meta_field = SelectField('Правило')
    date_start = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    alr_ip = StringField(
        'IP источника', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='IP источника')
    alr_node = SelectField('Источник')
    tax = StringField(
        'Таксономия', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Таксономия')

class EventForm(FlaskForm):
    search = StringField(
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Поиск',
        render_kw={"placeholder": "Поиск"})
    meta_field = SelectField('Источник')
    date_start = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    alr_ip = StringField(
        'IP источника', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='IP источника')
    tax = StringField(
        'Таксономия', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Таксономия')

class AlertForm(FlaskForm):
    search = StringField(
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Поиск',
        render_kw={"placeholder": "Поиск"})
    meta_field = SelectField('Источник')
    date_start = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    ip = StringField(
        'IP источника', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='IP источника')

class SearchForm(FlaskForm):
    search = StringField(
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Поиск',
        render_kw={"placeholder": "Фильтр"})
    meta_field = StringField('Мета поле')
    date_start = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(format='%Y-%m-%dT%H:%M')
