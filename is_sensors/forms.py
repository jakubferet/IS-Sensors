import os
import secrets
from PIL import Image
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField

from is_sensors import app


def new_picture(picture):
    size = (200, 200)
    random_name = 'img'+secrets.token_hex(4)
    _, ext = os.path.splitext(picture.filename)
    picture_name = random_name+ext
    picture_path = os.path.join(app.root_path, 'static\\images', picture_name)
    image = Image.open(picture)
    image.thumbnail(size)
    image.save(picture_path)
    return picture_name

def delete_old_picture(picture):
    if picture != 'default.png':
        old_picture = os.path.join(app.root_path, 'static\\images', picture)
        if os.path.exists(old_picture):
            os.remove(old_picture)

class SensorForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(min=4, max=25)])
    #price = IntegerField('Průměrná cena [Kč]')
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