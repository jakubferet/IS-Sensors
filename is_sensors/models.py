import datetime

from is_sensors import db

category_manufacturer = db.Table('production',
        db.Column('manufacturer_id', db.Integer, db.ForeignKey('manufacturer.id'), primary_key=True),
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    picture = db.Column(db.String, default='default.png')
    lastchange = db.Column(db.DateTime, default=datetime.datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'picture': self.picture,
            'category_id': self.category.id,
            'manufacturer_id': self.manufacturer.id,
            'category_name': self.category.name,
            'manufacturer_name': self.manufacturer.name
        }
        
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    picture = db.Column(db.String, default='default.png')
    lastchange = db.Column(db.DateTime, default=datetime.datetime.now)
    sensors = db.relationship('Sensor', backref='manufacturer', lazy=True)

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    picture = db.Column(db.String, default='default.png')
    lastchange = db.Column(db.DateTime, default=datetime.datetime.now)
    sensors = db.relationship('Sensor', backref='category', lazy=True)
    manufacturers = db.relationship('Manufacturer', secondary=category_manufacturer, backref='categories')

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture
        }

#db.drop_all()
db.create_all()