"""
    ZIEM

    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, PasswordField, SelectField, FieldList
from wtforms import TextAreaField, IntegerField
from wtforms import FormField, validators, BooleanField, SubmitField
from flask_wtf import FlaskForm

class LogForm(FlaskForm):
    class Meta:
        csrf = False
    logname = StringField(
        'Название', 
        [validators.Length(max=5000)],
        render_kw={
            'maxlength':5000,
            'class':'form-control', 
            'title':'Название журнала для сбора при активном подключении'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=20000)],
        render_kw={
            'maxlength':20000,
            'class':'form-control', 
            'title':'Краткое описание журнала'})
    normrule = SelectField(
        'Правило нормализации *',
        render_kw={
            'class':'form-select', 
            'title':'С помощью какой нормализации обрабатывать жунал'})


class RuleForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название источника в формате: SIKNXXX_ARM_OSN'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание источника'})
    ip = StringField(
        'IP адрес *', 
        [validators.Length(max=200)],
        render_kw={
            'required':"",
            'maxlength':200,
            'class':'form-control', 
            'title':'Адрес источника'})
    ip_rez = StringField(
        'IP резервный адрес', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Резервный адрес источника'})
    port = StringField(
        'PORT', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Порт источника'})
    port_rez = StringField(
        'PORT резервный', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Резервный порт источника'})
    login = SelectField(
        'Пользователь',
        render_kw={
            'class':'form-select', 
            'title':'Учетная запись для подключения к источнику'})
    protocol = SelectField(
        'Протокол *',
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Протокол для подключения к источнику',
            'onchange': 'change_protocol_log(this)'})
    port_rez = StringField(
        'PORT резервный', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Резервный порт источника'})
    net_flow = IntegerField(
        'Контроль потока', 
        [validators.Optional(), 
        validators.NumberRange(min=0)], 
        default=0,
        render_kw={
            'min':0,
            'class':'form-select',
            'title':'Период времени в часах для контроля потока сообщений'})
    active = BooleanField('Активный источник', default=False)
    obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Принадлежность инциента к объекту'})
    logs = FieldList(
        FormField(LogForm), 
        min_entries=1)
    
    sub = SelectField(
        'Система',
        [],
        render_kw={
            'class':'form-select', 
            'title':'Подсистема типа АСУТП'})
    
    type = SelectField(
        'Тип',
        [],
        render_kw={
            'class':'form-select', 
            'title':'Тип актива'})
    
    new_active = SubmitField('Создать актив', default=False,
                            render_kw={
            'class':'save btn btn-danger shadow border-0 form-control', 
            'title':'Создать новый актив на основе текущего шаблона'})

class CredForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название учетной записи'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание источника'})
    pswd = PasswordField(
        'Пароль *', 
        [validators.DataRequired()],
        description='Пароль',
        render_kw={
            'class':'form-control', 
            'title':'Пароль учетной записи'})
    obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Принадлежность инциента к объекту'})

class JsonForm(FlaskForm):
    jdata = TextAreaField(
        'Данные в формате JSON', 
        [validators.DataRequired(),
        validators.Length(min=10, max=500000, message="Длина не менее 10 символов")],
        description='Данные')
    backup = SelectField('Бэкап')
    obj = SelectField()

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
    selected_type = SelectField(
        'Тип *', 
        [validators.DataRequired()],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Тип актива'})
