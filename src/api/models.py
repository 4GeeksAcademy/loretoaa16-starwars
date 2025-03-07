from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String)

    def __repr__(self):
        return f'<User id: {self.id} - {self.email}>'

    def serialize(self):
          # do not serialize the password, its a security breach
        return {'id': self.id,
                'email': self.email,
                'is_active': self.is_active,
                'first_name': self.first_name,
                'last_name': self.last_name}

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    body = db.Column(db.String, unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    image_url = db.Column(db.String, unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('posts_to', lazy='select'))

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('comments_to', lazy='select'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post_to = db.relationship('Posts', foreign_keys=[post_id], backref=db.backref('comments_to', lazy='select'))

class Medias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.Enum('reel', 'image', 'video', name='type'), nullable=False)
    image_url = db.Column(db.String, unique=True, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post_to = db.relationship('Posts', foreign_keys=[post_id], backref=db.backref('medias_to', lazy='select'))


class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Columna clave foranea
    following_to =db.relationship('Users', foreign_keys=[following_id], backref=db.backref('following_to'), lazy='select') # La relación
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_to = db.relationship('Users', foreign_keys=[follower_id], backref=db.backref('follower_to'), lazy='select')

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    height = db.Column(db.String, nullable=True)
    mass = db.Column(db.String, nullable=True)
    hair_color = db.Column(db.String, nullable=True)
    skin_color = db.Column(db.String, nullable=True)
    eye_color = db.Column(db.String, nullable=True)
    birth_year = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)

class CharacterFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Columna clave foranea
    user_to =db.relationship('Users', foreign_keys=[user_id], backref=db.backref('CharacterFavorites_to'), lazy='select') # La relación
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character_to = db.relationship('Characters', foreign_keys=[character_id], backref=db.backref('CharacterFavorites_to'), lazy='select')

    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'character_id': self.character_id}

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    diameter = db.Column(db.String, nullable=True)
    rotation_period = db.Column(db.String, nullable=True)
    orbital_period = db.Column(db.String, nullable=True)
    gravity = db.Column(db.String, nullable=True)
    population = db.Column(db.String, nullable=True)
    climate = db.Column(db.String, nullable=True)
    terrain = db.Column(db.String, nullable=True)

class PlanetFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Columna clave foranea
    user_to =db.relationship('Users', foreign_keys=[user_id], backref=db.backref('PlanetFavorites_to'), lazy='select') # La relación
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_to = db.relationship('Planets', foreign_keys=[planet_id], backref=db.backref('PlanetsFavorites_to'), lazy='select')
    
    def serialize(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'planet_id': self.planet_id}


"""
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product: {self.id} - {self.name}>'

class Bills(db.Model):
    __tablename__='bills'
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #default, creation day
    total = db.Column(db.Float, nullable=False)
    bill_address = db.Column(db.String)
    status = db.Column(db.Enum('pending', 'paid', 'cancel', name='status'), nullable=False)
    payment = db.Column(db.Enum('visa', 'amex', 'paypal', name='payment'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('bills_to', lazy='select'))

    def __repr__(self):
        return f'<Bills: {self.id} - user: {self.user_id}>'

class BillItems(db.Model):
    __tablename__='bills_items'
    id = db.Column(db.Integer, primary_key=True)
    price_per_unit = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'))
    bill_to = db.relationship('Bills', foreign_keys=[bill_id], backref=db.backref('bills_items', lazy='select'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_to = db.relationship('Products', foreign_keys=[product_id], backref=db.backref('bill_items', lazy='select'))

    def __repr__(self):
        return f'<Bill {self.bill_id} items: {self.id} product: {self.product_id}>'
"""


