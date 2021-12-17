from flask import Blueprint, request, jsonify
from models import db, Client
from schemas import client_schema, clients_schema

import datetime

clients = Blueprint('clients', __name__)


@clients.route('/clients', methods=['GET'])
def index_clients():
    query = Client.query.all()
    clients = clients_schema.dump(query)
    
    return jsonify(clients)

@clients.route('/clients', methods=['POST'])
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

@clients.route('/clients/<id>', methods=['GET'])
def show_client(id):
    client = Client.query.get(id)    
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)    
    
@clients.route('/search_client/<dni>', methods=['GET'])
def get_client_for_dni(dni):
    client = Client.query.filter_by(document_number=dni).first()
    
    if client is None:
        return 'Client not found', 404
    
    return client_schema.jsonify(client)

@clients.route('/search_senders', methods=['GET'])
def get_clients_senders_rol():
    senders = Client.query.filter_by(rol='REMITENTE').all()
    
    return clients_schema.jsonify(senders)

