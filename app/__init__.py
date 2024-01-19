# from flask import Flask, request, jsonify
# from config import Config
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from werkzeug.security import generate_password_hash, check_password_hash
# from forms import UserLoginForm
# from flask import redirect, url_for, flash
# from models import User, db, login_manager, ma
# from flask_login import login_user, logout_user, LoginManager, current_user, login_required


# import secrets

# app = Flask(__name__)
# CORS(app)
# app.config.from_object(Config)
# db.init_app(app)
# login_manager.init_app(app)
# ma.init_app(app)
# migrate = Migrate(app, db)

# @app.route('/getdata')
# def getdata():
#     return {'yee':'haa'}


# @app.route("/signup", methods=['POST'])
# def userRegister():
#     user = User.query.filter_by(email=request.json['email']).first()
#     if user:
#         return jsonify(message='Email already exists'), 401
#     first_name = request.json['first_name']
#     last_name = request.json['last_name']
#     email = request.json['email']
#     password = request.json['password']
#     new_user = User(email,first_name,last_name,password)
#     db.session.add(new_user)
#     db.session.commit()
#     response = {
#         'id': new_user.id,
#         'first_name': new_user.first_name,
#         'last_name': new_user.last_name,
#         'email': new_user.email,
#         'password': new_user.password,
#         'token': new_user.token
#     }
#     return jsonify(response)

# @app.route("/login", methods=['POST'])
# def userLogin():
#     email = request.json['email']
#     password = request.json['password']
#     user = User.query.filter_by(email=email).first()
#     if user and check_password_hash(user.password, password):
#         access_token = user.token
#         return jsonify(token=access_token), 201
#     return jsonify(message='Invalid Username/Password'), 401

# @app.route("/logout", methods=['POST'])
# def logoutUser():
#     token = request.json['auth']
#     user = User.query.filter(User.token==token).first()
#     if user:
#         user.token = ''
#         db.session.commit()
#         return jsonify(message='Logout Successful!'), 201
#     return jsonify(message='Something went wrong!'), 401


#  logout_user()
#     return redirect('/userLogin')
#     #TODO: return What?
    

# app.config.from_object(Config)

from flask import Flask, render_template
from config import Config
# from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
# app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)