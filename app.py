from flask import Flask
from blueprints.clients import clients
from blueprints.users import users
#import read_pdf_service
from models import db
from schemas import ma
from config import config

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    
    with app.app_context():
        ma.init_app(app)
        db.init_app(app)
        db.create_all()
        
    app.register_blueprint(clients)
    app.register_blueprint(users)
    
    return app

enviroment = config['development']
app = create_app(enviroment)     

### Routes ###
@app.route('/')
def homeView():
    return 'HOME VIEW'

'''@app.route('/read_pdf')
def read_pdf():
    return read_pdf_service.read('giro4.pdf')'''

if __name__ == '__main__':
    app.run()