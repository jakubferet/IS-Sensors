from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField

class SensorForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(min=4, max=25)])
    price = IntegerField('Průměrná cena [Kč]')
    description = TextAreaField('Popis')
    picture = FileField('Vložit obrázek', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Kategorie', coerce=int)
    manufacturer = SelectField('Výrobce', coerce=int)
    submit = SubmitField('Odeslat')

class ManufacturerForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(min=4, max=25)])
    description = TextAreaField('Popis')
    picture = FileField('Vložit obrázek', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Odeslat')

class CategoryForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(min=4, max=25)])
    description = TextAreaField('Popis')
    picture = FileField('Vložit obrázek', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Odeslat')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Hledat')