from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph

db = SQLAlchemy()

### User ###
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
 

### Client ###   
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
