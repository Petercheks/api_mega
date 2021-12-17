from flask_marshmallow import Marshmallow

ma = Marshmallow()

### Schemas ###
class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id','firstname','lastname','document_number','document_type','rol','phone_number','created_at')
client_schema = ClientSchema()   
clients_schema = ClientSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields =('id','firstname','lastname','email','password','created_at')
user_schema = UserSchema()
users_schema = UserSchema(many=True)  