from flask import Blueprint, request
from models import db, User
from schemas import user_schema, users_schema
from werkzeug.security import generate_password_hash as genph

import datetime

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def index_users():
    users = User.query.all()    
    return users_schema.jsonify(users)

@users.route('/users', methods=['POST'])
def create_user():    
    try:
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        password = genph(request.json['password'])        
        created_at = datetime.datetime.now()

        new_user = User(firstname, lastname, email, password, created_at)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)
    
    except Exception:
        return "User not save", 400
    
@users.route('/users/<userId>', methods=['GET'])
def show_user(userId):
    user = User.query.get(userId)
    
    if user is None:
        return 'User not found', 404
    
    return user_schema.jsonify(user)

@users.route('/users/<userId>', methods=['PUT'])
def update_user(userId):
    try:
        user = User.query.get(userId)

        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        password = genph(request.json['password'])

        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.password = password
        db.session.commit()
        
        return user_schema.jsonify(user)
    
    except:
        return "User doesn't updated", 400

@users.route('/users/<userId>', methods=['DELETE'])
def user_destroy(userId):    
    try:
        user = User.query.get(userId)        
        db.session.delete(user)
        db.session.commit()
        
        return user_schema.jsonify(user)
    except:
        return "User doesn't exist", 400
    
    
    