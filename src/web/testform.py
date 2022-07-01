"""
    ZIEM

    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import TextAreaField, StringField, PasswordField, IntegerField
from wtforms import validators
from flask_wtf import FlaskForm

class JsonForm(FlaskForm):
    jdata = TextAreaField(
        'Данные в формате JSON', 
        [validators.DataRequired(),
        validators.Length(min=10, max=500000, message="Длина не менее 10 символов")],
        description='Данные')

class WmiForm(FlaskForm):
    ip = StringField(
        'IP адрес', 
        [validators.DataRequired(),
        validators.Length(max=15, message="Длина не более 15 символов")],
        description='IP адрес')
    username = StringField(
        'Пользователь', 
        [validators.Length(max=15, message="Длина не более 15 символов")],
        description='Пользователь')
    pswd = PasswordField(
        'Пароль', 
        [validators.Length(max=25, message="Длина не более 25 символов")],
        description='Пароль')

class FtpForm(FlaskForm):
    ip = StringField(
        'IP адрес', 
        [validators.DataRequired(),
        validators.Length(max=15, message="Длина не более 15 символов")],
        description='IP адрес')
    username = StringField(
        'Пользователь', 
        [validators.Length(max=15, message="Длина не более 15 символов")],
        description='IP адрес')
    pswd = PasswordField(
        'Пароль', 
        [validators.Length(max=25, message="Длина не более 25 символов")],
        description='Пароль')
    log = StringField(
        'Журнал', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='Журнал')
    port = StringField(
        'Порт', 
        description='IP адрес')

class NmapForm(FlaskForm):
    ip = StringField(
        'IP адрес', 
        [validators.DataRequired(),
        validators.Length(max=21, message="Длина не более 21 символов")],
        description='IP адрес')
    port = StringField('Port')

class OpcuaForm(FlaskForm):
    ip = StringField(
        'IP адрес', 
        [validators.DataRequired(),
        validators.Length(max=15, message="Длина не более 15 символов")],
        description='IP адрес')
    username = StringField(
        'Пользователь', 
        [validators.Length(max=15, message="Длина не более 15 символов")],
        description='Пользователь')
    pswd = PasswordField(
        'Пароль', 
        [validators.Length(max=25, message="Длина не более 25 символов")],
        description='Пароль')
    log = StringField(
        'OPC UA Tag', 
        [validators.Length(max=50, message="Длина не более 50 символов")],
        description='OPC UA Tag')
    port = StringField()

class TestForm(FlaskForm):
    ip = StringField('IP адрес')
    username = StringField('Пользователь')
    pswd = PasswordField('Пароль')
    log = StringField('Журнал')
    port = StringField('Port')