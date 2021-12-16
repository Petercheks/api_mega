from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import datetime
import read_pdf_service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/api_giros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Models
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
    
client_schema = ClientSchema()   
clients_schema = ClientSchema(many=True)

#Routes
@app.route('/')
def homeView():
    return 'HOME VIEW'

@app.route('/read_pdf')
def read_pdf():
    return read_pdf_service.read('giro4.pdf')

@app.route('/clients', methods=['GET'])
def index_clients():
    query = Clients.query.all()
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

        new_client = Clients(firstname, lastname, document_number, document_type, rol, phone_number, created_at)
        db.session.add(new_client)
        db.session.commit()

        return client_schema.jsonify(new_client)
    
    except Exception:
        return "Client not save", 400

@app.route('/clients/<id>', methods=['GET'])
def show_client(id):
    client = Clients.query.get(id)    
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)    
    
@app.route('/search_client/<dni>', methods=['GET'])
def get_client_for_dni(dni):
    client = Clients.query.filter_by(document_number=dni).first()
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)

@app.route('/search_senders', methods=['GET'])
def get_clients_senders_rol():
    senders = Clients.query.filter_by(rol='REMITENTE').all()
    
    return clients_schema.jsonify(senders)


if __name__ == '__main__':
    app.run(debug=True)