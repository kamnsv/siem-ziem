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
