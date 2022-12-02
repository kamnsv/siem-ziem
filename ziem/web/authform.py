"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    user = StringField(
        'Логин', 
        [validators.DataRequired(),
        validators.Length(min=4, max=25, message="Длина не менее 4 символов")],
        description='Логин')
    pswd = PasswordField(
        'Пароль', 
        [validators.DataRequired(),
        validators.Length(min=4, max=25, message="Длина не менее 4 символов")],
        description='Пароль')

class CredForm(FlaskForm):
    name = StringField(
        'Пользователь *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50, message="Длина не менее 4 символов")],
        description='Пользователь')
    desc = StringField(
        'Описание *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=200, message="Длина не менее 4 символов")],
        description='Описание')
    pswd = PasswordField(
        'Пароль *', 
        [validators.DataRequired(),
        validators.Length(min=10, max=25, message="Длина не менее 10 символов")],
        description='Пароль')

class SearchForm(FlaskForm):
    searchInput = StringField(
        'Фильтр', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':''})
