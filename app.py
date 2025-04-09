from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTDecodeError

from routes.category_route import category_bp
from routes.equipment_type_route import equipment_type_bp
from routes.equipments_route import equipments_bp
from routes.location_route import location_bp
from routes.stock_route import stock_bp
from routes.user_route import user_bp
from marshmallow.exceptions import ValidationError
import os
import time

load_dotenv()

JWT_ISSUED_AT_MIN = int(time.time())

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['TESTING'] = False

    JWTManager(app)

    app.register_blueprint(stock_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(equipment_type_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(equipments_bp)

    #swagger = Swagger(app)

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
                    return jsonify({"message": "Token expirado. Faça login novamente."}), 401
        except (NoAuthorizationError, JWTDecodeError):
            pass

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({'message': error.messages})

    return app
