from flask import Flask, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from routes.estoque_routes import estoque_bp
from routes.user_route import user_bp
from marshmallow.exceptions import ValidationError
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

jwt = JWTManager(app)

app.register_blueprint(estoque_bp)
app.register_blueprint(user_bp)

#swagger = Swagger(app)

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'message': error.messages})
