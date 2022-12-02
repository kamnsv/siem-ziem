"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

from wtforms import StringField, PasswordField, SelectField, FieldList, TextAreaField
from wtforms import FormField, validators, SelectMultipleField
from wtforms import Form
from flask_wtf import FlaskForm

class RegexForm(Form):
    class Meta:
        csrf = False
        
    value = StringField(
        'Искомая строка', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Что необходимо искать либо номер элемента'})
    field = SelectField(
        'Поле',
        render_kw={
            'class':'form-select', 
            'title':'Какому полю присваивается найденое значение'})


class EventForm(Form):
    class Meta:
        csrf = False

    string = StringField(
        'Искомая строка', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Что необходимо искать либо ID события'})
    alr_msg = StringField(
        'Событие', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Название новому событию'})
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
    regex = FieldList(
        FormField(RegexForm), 
        min_entries=1)


class RuleForm(FlaskForm):
    name = StringField(
        'Название *', 
        [validators.DataRequired(),
        validators.Length(min=4, max=50)],
        render_kw={
            'minlength':4,
            'maxlength':50,
            'class':'form-control', 
            'title':'Название правила в формате: ARM_Windows-10'})
    desc = StringField(
        'Описание', 
        [validators.Length(max=200)],
        render_kw={
            'maxlength':200,
            'class':'form-control', 
            'title':'Краткое описание правила'})
    profile = SelectField(
        'Профиль *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'По какому профилю нормализовывать события'})
    tax_main = SelectField(
        'Таксономия основная',
        render_kw={
            'class':'form-select', 
            'title':'К какому объекту относится событие'})
    obj = SelectField(
        'Объект *', 
        [validators.DataRequired()],
        render_kw={
            'class':'form-select', 
            'title':'Принадлежность инциента к объекту'})
    events = FieldList(
        FormField(EventForm), 
        min_entries=1)

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
