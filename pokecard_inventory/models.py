from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default = '')
    last_name = db.Column(db.String(150), nullable=True, default = '')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False, default = '')
    username = db.Column(db.String, nullable=False)
    token = db.Column(db.String, default = '', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    poke_card = db.relationship('Poke_Card', backref = 'owner', lazy=True)

    def __init__(self, email, username, password, first_name='', last_name=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f'User {self.email} has been added to the database!'
    
class Poke_Card(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    series = db.Column(db.String(150))
    year = db.Column(db.Integer, nullable=False)
    collector_card_number = db.Column(db.String(150), nullable=False)
    is_graded = db.Column(db.String(150), nullable=True)
    grade = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    for_sale = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)


    def __init__(self, name, type, series, year, collector_card_number, is_graded, grade, description, for_sale, user_token):
        self.id = self.set_id()
        self.name = name
        self.type = type
        self.series = series
        self.year = year
        self.collector_card_number = collector_card_number
        self.is_graded = is_graded
        self.grade = grade
        self.description = description
        self.for_sale = for_sale
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'Your {self.name} has been added to the database!'
    

class PokeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'type', 'series', 'year', 'collector_card_number', 'is_graded', 'grade', 'description', 'for_sale']

poke_schema = PokeSchema()
pokes_schema = PokeSchema(many=True)