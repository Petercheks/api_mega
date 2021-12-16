from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# Client Model

class Clients(db.Model):
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

db.create_all()

class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id','firstname','lastname','document_number','document_type','rol','phone_number','created_at')
    
