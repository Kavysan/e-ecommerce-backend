from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets
from sqlalchemy.dialects.postgresql import ARRAY

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    # token = db.Column(db.String, default='', unique=True)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return [secrets.token_hex(length)]

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150), nullable = False)
    model = db.Column(db.String(200))
    year = db.Column(db.String(20))
    color = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,make,model,year,color,user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.user_token = user_token


    def __repr__(self):
        return f'The following car has been added to the inventory: {self.make}, {self.model}'

    def set_id(self):
        return (secrets.token_urlsafe())
    
class UserSchema(ma.Schema):    
    class Meta:
        fields = ['id', 'first_name','last_name','email','password','token']
user_schema = UserSchema()


class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make','model','year', 'color']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)