from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTDecodeError
from peewee import SqliteDatabase

from database.create_tables import create_all_tables
from routes.category_route import category_bp
from routes.equipment_type_route import equipment_type_bp
from routes.equipments_route import equipments_bp
from routes.location_route import location_bp
from routes.movement_history_route import movement_bp
from routes.stock_route import stock_bp
from routes.user_route import user_bp
from marshmallow.exceptions import ValidationError
from database.db import db, get_postgres_database
import os
import time

load_dotenv()

JWT_ISSUED_AT_MIN = int(time.time())

def create_app(testing=False):
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    if testing:
        app.config["TESTING"] = True
        test_db = SqliteDatabase(':memory:')
        db.initialize(test_db)
        from database.create_tables import create_all_tables
        create_all_tables(testing=True)
    else:
        from database.create_tables import create_all_tables
        db.initialize(get_postgres_database())
        create_all_tables(testing=False)

    JWTManager(app)

    app.register_blueprint(stock_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(equipment_type_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(equipments_bp)
    app.register_blueprint(movement_bp)

    Swagger(app)

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
