from sqlalchemy import func
from flask_breadcrumbs import register_breadcrumb
from flask import render_template, url_for, redirect, flash, request

from is_sensors import app, db
from is_sensors.models import Sensor, Manufacturer, Category
from is_sensors.forms import SensorForm, ManufacturerForm, CategoryForm, SearchForm, new_picture, delete_old_picture


@app.route("/")
@app.route("/home")
@register_breadcrumb(app, '.', 'Domů')
def home():
    sensors = Sensor.query.limit(5).all()
    categories = Category.query.limit(5).all()
    manufacturers = Manufacturer.query.limit(5).all()
    return render_template('home.html', sensors=sensors, categories=categories, manufacturers=manufacturers, hideBreadcrumbs=True)

@app.context_processor
def searchBar():
    form = SearchForm()
    return dict(form=form)

@app.route("/search", methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.search.data
        sensors = Sensor.query.filter(func.upper(Sensor.name).contains(func.upper(searched))).all()
        categories = Category.query.filter(func.upper(Category.name).contains(func.upper(searched))).all()
        manufacturers = Manufacturer.query.filter(func.upper(Manufacturer.name).contains(func.upper(searched))).all()
        return render_template('search.html', searched=searched, sensors=sensors, categories=categories, manufacturers=manufacturers, form=form, hideBreadcrumbs=True)

@app.route("/sensors/data")
def sensorsData():
    sensors = Sensor.query.all()
    data = {'data': [sensor.toDict() for sensor in sensors]}
    return data

@app.route("/sensors")
@register_breadcrumb(app, '.sensors', 'Čidla')
def sensors():
    url_data = url_for('sensorsData')
    return render_template('table.html', url_data=url_data)

def get_sensor_name():
    id = request.view_args['id']
    sensor = Sensor.query.get(id)
    return [{'text': sensor.name, 'url': url_for('readSensor', id=id)}]

@app.route("/sensor/<int:id>")
@register_breadcrumb(app, '.sensors.sensor', '', dynamic_list_constructor=get_sensor_name)
def readSensor(id):
    sensor = Sensor.query.get_or_404(id)
    return render_template('entry.html', item=sensor, type='sensor', update='updateSensor', delete='deleteSensor')

@app.route("/sensor/create", methods=['GET', 'POST'])
@register_breadcrumb(app, '.sensors.create', 'Přidat nové čidlo')
def createSensor():
    form = SensorForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.order_by('name')]
    form.manufacturer.choices = [(manufacturer.id, manufacturer.name) for manufacturer in Manufacturer.query.order_by('name')]
    if form.validate_on_submit():
        sensor = Sensor(name=form.name.data, description=form.description.data, manufacturer_id=form.manufacturer.data, category_id=form.category.data)
        category = Category.query.get_or_404(form.category.data)
        manufacturer = Manufacturer.query.get_or_404(form.manufacturer.data)
        category.manufacturers.append(manufacturer)
        if form.picture.data:
            picture_file = new_picture(form.picture.data)
            sensor.picture = picture_file
        db.session.add(sensor)
        db.session.add(category)
        db.session.commit()
        flash('Bylo přidáno nové čidlo.', 'success')
        return redirect(url_for('sensors'))
    return render_template('user_input.html', title='Přidat nové čidlo', form=form)

@app.route("/sensor/<int:id>/update", methods=['GET', 'POST'])
@register_breadcrumb(app, '.sensors.sensor.update', 'Aktualizovat čidlo')
def updateSensor(id):
    sensor = Sensor.query.get_or_404(id)
    form = SensorForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.order_by('name')]
    form.manufacturer.choices = [(manufacturer.id, manufacturer.name) for manufacturer in Manufacturer.query.order_by('name')]
    picture = sensor.picture
    if request.method == 'GET':
        form.name.data = sensor.name
        form.description.data = sensor.description
        form.category.data = sensor.category_id
        form.manufacturer.data = sensor.manufacturer_id
    elif form.validate_on_submit():
        sensor.name = form.name.data
        sensor.description = form.description.data
        sensor.category_id = form.category.data
        sensor.manufacturer_id = form.manufacturer.data
        if form.picture.data:
            delete_old_picture(picture)
            picture_file = new_picture(form.picture.data)
            sensor.picture = picture_file
        db.session.commit()
        flash('Čidlo bylo aktualizováno.', 'success')
        return redirect(url_for('readSensor', id=sensor.id))
    return render_template('user_input.html', title='Aktualizovat čidlo', picture=picture, form=form)

@app.route("/sensor/<int:id>/delete", methods=['POST'])
def deleteSensor(id):
    sensor = Sensor.query.get_or_404(id)
    picture = sensor.picture
    delete_old_picture(picture)
    db.session.delete(sensor)
    db.session.commit()
    flash('Čidlo bylo odstraněno.', 'success')
    return redirect(url_for('sensors'))

@app.route("/categories")
@register_breadcrumb(app, '.categories', 'Kategorie')
def categories():
    categories = Category.query.all()
    return render_template('all_entries.html', items=categories, read='readCategory', create='createCategory', title='Kategorie', new='Nová kategorie')

def get_category_name():
    id = request.view_args['id']
    category = Category.query.get(id)
    return [{'text': category.name, 'url': url_for('readCategory', id=id)}]

@app.route("/category/<int:id>")
@register_breadcrumb(app, '.categories.category', '', dynamic_list_constructor=get_category_name)
def readCategory(id):
    category = Category.query.get_or_404(id)
    return render_template('entry.html', item=category, type='category', update='updateCategory', delete='deleteCategory')

@app.route("/category/create", methods=['GET', 'POST'])
@register_breadcrumb(app, '.categories.create', 'Přidat novou kategorii')
def createCategory():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data)
        if form.picture.data:
            picture_file = new_picture(form.picture.data)
            category.picture = picture_file
        db.session.add(category)
        db.session.commit()
        flash('Byla přidána nová kategorie.', 'success')
        return redirect(url_for('categories'))
    return render_template('user_input.html', title='Přidat novou kategorii', form=form)

@app.route("/category/<int:id>/update", methods=['GET', 'POST'])
@register_breadcrumb(app, '.categories.category.update', 'Aktualizovat kategorii')
def updateCategory(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    picture = category.picture
    if request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    elif form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        if form.picture.data:
            delete_old_picture(picture)
            picture_file = new_picture(form.picture.data)
            category.picture = picture_file
        db.session.commit()
        flash('Kategorie byla aktualizována.', 'success')
        return redirect(url_for('readCategory', id=category.id))
    return render_template('user_input.html', title='Aktualizovat kategorii', picture=picture, form=form)

@app.route("/category/<int:id>/delete", methods=['POST'])
def deleteCategory(id):
    category = Category.query.get_or_404(id)
    picture = category.picture
    delete_old_picture(picture)
    db.session.delete(category)
    db.session.commit()
    flash('Kategorie byla odstraněna.', 'success')
    return redirect(url_for('categories'))

@app.route("/category/<int:id>/sensors/data")
def category_sensors_data(id):
    sensors = Sensor.query.filter_by(category_id=id).all()
    data = {'data': [sensor.toDict() for sensor in sensors]}
    return data

@app.route("/category/<int:id>/sensors")
@register_breadcrumb(app, '.categories.category.sensors', 'Čidla')
def category_sensors(id):
    category = Category.query.get_or_404(id)
    url_data = url_for('category_sensors_data', id=id)
    return render_template('table.html', url_data=url_data, title=f'Čidla kategorie <strong>{category.name}</strong>')

@app.route("/category/<int:id>/manufacturers")
@register_breadcrumb(app, '.categories.category.manufacturers', 'Výrobci')
def category_manufacturers(id):
    category = Category.query.get_or_404(id)
    manufacturers = Manufacturer.query.filter(Manufacturer.categories.contains(category)).all()
    return render_template('all_entries.html', items=manufacturers, read='readManufacturer', create='createManufacturer', title=f'Výrobci kategorie {category.name}', new='Nový výrobce')

@app.route("/manufacturers")
@register_breadcrumb(app, '.manufacturers', 'Výrobci')
def manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('all_entries.html', items=manufacturers, read='readManufacturer', create='createManufacturer', title='Výrobci', new='Nový výrobce')

def get_manufacturer_name():
    id = request.view_args['id']
    manufacturer = Manufacturer.query.get(id)
    return [{'text': manufacturer.name, 'url': url_for('readManufacturer', id=id)}]

@app.route("/manufacturer/<int:id>")
@register_breadcrumb(app, '.manufacturers.manufacturer', '', dynamic_list_constructor=get_manufacturer_name)
def readManufacturer(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    return render_template('entry.html', item=manufacturer, type='manufacturer', update='updateManufacturer', delete='deleteManufacturer')

@app.route("/manufacturer/create", methods=['GET', 'POST'])
@register_breadcrumb(app, '.manufacturers.create', 'Přidat nového výrobce')
def createManufacturer():
    form = ManufacturerForm()
    if form.validate_on_submit():
        manufacturer = Manufacturer(name=form.name.data, description=form.description.data)
        if form.picture.data:
            picture_file = new_picture(form.picture.data)
            manufacturer.picture = picture_file
        db.session.add(manufacturer)
        db.session.commit()
        flash('Byl přidán nový výrobce.', 'success')
        return redirect(url_for('manufacturers'))
    return render_template('user_input.html', title='Přidat nového výrobce', form=form)

@app.route("/manufacturer/<int:id>/update", methods=['GET', 'POST'])
@register_breadcrumb(app, '.manufacturers.manufacturer.update', 'Aktualizovat výrobce')
def updateManufacturer(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    form = ManufacturerForm()
    picture = manufacturer.picture
    if request.method == 'GET':
        form.name.data = manufacturer.name
        form.description.data = manufacturer.description
    elif form.validate_on_submit():
        manufacturer.name = form.name.data
        manufacturer.description = form.description.data
        if form.picture.data:
            delete_old_picture(picture)
            picture_file = new_picture(form.picture.data)
            manufacturer.picture = picture_file
        db.session.commit()
        flash('Výrobce byl aktualizován.', 'success')
        return redirect(url_for('readManufacturer', id=manufacturer.id))
    return render_template('user_input.html', title='Aktualizovat výrobce', picture=picture, form=form)

@app.route("/manufacturer/<int:id>/delete", methods=['POST'])
def deleteManufacturer(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    picture = manufacturer.picture
    delete_old_picture(picture)
    db.session.delete(manufacturer)
    db.session.commit()
    flash('Výrobce byl odstraněn.', 'success')
    return redirect(url_for('manufacturers'))

@app.route("/manufacturer/<int:id>/sensors/data")
def manufacturer_sensors_data(id):
    sensors = Sensor.query.filter_by(manufacturer_id=id).all()
    data = {'data': [sensor.toDict() for sensor in sensors]}
    return data

@app.route("/manufacturer/<int:id>/sensors")
@register_breadcrumb(app, '.manufacturers.manufacturer.sensors', 'Čidla')
def manufacturer_sensors(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    url_data = url_for('manufacturer_sensors_data', id=id)
    return render_template('table.html', url_data=url_data, title=f'Čidla od výrobce <strong>{manufacturer.name}</strong>')

@app.route("/manufacturer/<int:id>/categories")
@register_breadcrumb(app, '.manufacturers.manufacturer.categories', 'Kategorie')
def manufacturer_categories(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    categories = Category.query.filter(Category.manufacturers.contains(manufacturer)).all()
    return render_template('all_entries.html', items=categories, read='readCategory', create='createCategory', title=f'Kategorie od výrobce {manufacturer.name}', new='Nová kategorie')

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', hideBreadcrumbs=True), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', hideBreadcrumbs=True), 500