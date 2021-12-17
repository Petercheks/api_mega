import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph

import datetime
import read_pdf_service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/api_giros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

### Models ###
class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    document_number = db.Column(db.Integer, unique=True)
    document_type = db.Column(db.String(50))
    rol = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    
    def __init__(self, firstname, lastname, document_number, document_type, rol, phone_number, created_at ):
        self.firstname = firstname
        self.lastname = lastname
        self.document_number = document_number
        self.document_type = document_type
        self.rol = rol
        self.phone_number = phone_number
        self.created_at = created_at
        
class User(db.Model):    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime)
    
    def __init__(self, firstname, lastname, email, password, created_at ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.created_at = created_at
    
    def def_clave(self, clave):
        self.password = genph(clave)

    def verif_clave(self, clave):
        return checkph(self.password, clave)

db.create_all()

class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id','firstname','lastname','document_number','document_type','rol','phone_number','created_at')

class UserSchema(ma.Schema):
    class Meta:
        fields =('id','firstname','lastname','email','password','created_at')
        
### Schema ###
client_schema = ClientSchema()   
clients_schema = ClientSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

### Routes ###
@app.route('/')
def homeView():
    return 'HOME VIEW'

@app.route('/read_pdf')
def read_pdf():
    return read_pdf_service.read('giro4.pdf')


#----------Client Routes---------------#
@app.route('/clients', methods=['GET'])
def index_clients():
    query = Client.query.all()
    clients = clients_schema.dump(query)
    
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def create_client():    
    try:
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        document_number = request.json['document_number']
        document_type = request.json['document_type']
        rol = request.json['rol'],
        phone_number = request.json['phone_number']
        created_at = datetime.datetime.now()

        new_client = Client(firstname, lastname, document_number, document_type, rol, phone_number, created_at)
        db.session.add(new_client)
        db.session.commit()

        return client_schema.jsonify(new_client)
    
    except Exception:
        return "Client not save", 400

@app.route('/clients/<id>', methods=['GET'])
def show_client(id):
    client = Client.query.get(id)    
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)    
    
@app.route('/search_client/<dni>', methods=['GET'])
def get_client_for_dni(dni):
    client = Client.query.filter_by(document_number=dni).first()
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)

@app.route('/search_senders', methods=['GET'])
def get_clients_senders_rol():
    senders = Client.query.filter_by(rol='REMITENTE').all()
    
    return clients_schema.jsonify(senders)


#----------User Routes---------------#
@app.route('/users', methods=['GET'])
def index_users():
    users = User.query.all()    
    return users_schema.jsonify(users)

@app.route('/users', methods=['POST'])
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
    
@app.route('/users/<userId>', methods=['GET'])
def show_user(userId):
    user = User.query.get(userId)
    
    if user is None:
        return 'User not found', 404
    
    return user_schema.jsonify(user)

@app.route('/users/<userId>', methods=['PUT'])
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

@app.route('/users/<userId>', methods=['DELETE'])
def user_destroy(userId):    
    try:
        user = User.query.get(userId)        
        db.session.delete(user)
        db.session.commit()
        
        return user_schema.jsonify(user)
    except:
        return "User doesn't exist", 400
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)