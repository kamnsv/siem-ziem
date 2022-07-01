"""
    ZIEM
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, PasswordField, SelectField, FieldList, IntegerField
from wtforms import FormField, validators, TextAreaField
from flask_wtf import FlaskForm
from wtforms import Form

class FastruleForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название правила в формате: ARM_UserAdd'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание правила'})
    tax_main = SelectField(
        'Таксономия основная',
        render_kw={
            'class':'form-select', 
            'title':'К какому объекту относится событие'})
    tax_object = SelectField(
        'Таксономия объект',
        render_kw={
            'class':'form-select', 
            'title':'Какой объект подвержен/совершает действие'})
    tax_action = SelectField(
        'Таксономия действие',
        render_kw={
            'class':'form-select', 
            'title':'Какое действие совершается'})
    crit = SelectField(
        'Критичность', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Уровень критичности инцидента'})
    clas = SelectField(
        'Классификатор',
        render_kw={
            'class':'form-select', 
            'title':'Класс инцидента согласно перечню'})
    obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Принадлежность инциента к объекту'})

class IncfilterForm(Form):
    class Meta:
        csrf = False

    value = StringField(
        'Значение', 
        [validators.Length(max=20000)],
        render_kw={
            'maxlength':20000,
            'class':'form-control', 
            'title':'Значение поля при фильтрации'})
    field = SelectField(
        'Поле',
        render_kw={
            'class':'form-select', 
            'title':'Поле по которому событие принимается'})

class ExcfilterForm(Form):
    class Meta:
        csrf = False

    value = StringField(
        'Значение', 
        [validators.Length(max=20000)],
        render_kw={
            'maxlength':20000,
            'class':'form-control', 
            'title':'Значение поля при фильтрации'})
    field = SelectField(
        'Поле',
        render_kw={
            'class':'form-select', 
            'title':'Поле по которому событие исключается'})

class EventForm(Form):
    class Meta:
        csrf = False

    tax_main = SelectField(
        'Таксономия основная',
        render_kw={
            'class':'form-select', 
            'title':'К какому объекту относится событие'})
    tax_object = SelectField(
        'Таксономия объект',
        render_kw={
            'class':'form-select', 
            'title':'Какое объект подвержен/совершает действие'})
    tax_action = SelectField(
        'Таксономия действие',
        render_kw={
            'class':'form-select', 
            'title':'Какое действие совершается'})
    diff = SelectField(
        'Контроль',
        render_kw={
            'class':'form-select', 
            'title':'Какое поле контролировать на изменение значения'})
    count = IntegerField(
        'Агрегация',
        [validators.Optional(), 
        validators.NumberRange(min=0)], 
        default=0,
        render_kw={
            'min':0,
            'class':'form-control', 
            'title':'Количество необходимых событий для сработки правила'})
    incfilter = FieldList(FormField(IncfilterForm), min_entries=1)
    excfilter = FieldList(FormField(ExcfilterForm), min_entries=1)

class DeepruleForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название правила в формате: ARM_UserAdd'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание правила'})
    crit = SelectField(
        'Критичность', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Уровень критичности инцидента'})
    clas = SelectField(
        'Классификатор',
        render_kw={
            'class':'form-select', 
            'title':'Класс инцидента согласно перечню'})
    obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Принадлежность инциента к объекту'})
    uniq1 = SelectField(
        'Уникальное поле 1', 
        render_kw={
            'class':'form-select', 
            'title':'Разделение инцидента по отличающимся полям'})
    uniq2 = SelectField(
        'Уникальное поле 2', 
        render_kw={
            'class':'form-select', 
            'title':'Разделение инцидента по отличающимся полям'})
    timer = IntegerField(
        'Таймер', 
        [validators.Optional(), 
        validators.NumberRange(min=0)], 
        default=0,
        render_kw={
            'min':0,
            'class':'form-control',
            'title':'Период времени за который должны произойти события'})
    events = FieldList(FormField(EventForm), min_entries=1)

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
