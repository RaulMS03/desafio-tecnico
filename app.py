from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTDecodeError

from routes.stock_routes import stock_bp
from routes.user_route import user_bp
from marshmallow.exceptions import ValidationError
import os
import time

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)

JWT_ISSUED_AT_MIN = int(time.time())

@app.before_request
def check_expired_token():
    public_paths = ['/auth/register', '/auth/login']
    if request.path in public_paths:
        return

    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if claims:
            token_iat = claims.get("iat", 0)
            if token_iat < JWT_ISSUED_AT_MIN:
                return jsonify({"msg": "Token expirado. Faça login novamente."}), 401
    except (NoAuthorizationError, JWTDecodeError):
        pass

app.register_blueprint(stock_bp)
app.register_blueprint(user_bp)

#swagger = Swagger(app)

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'message': error.messages})
