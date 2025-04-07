from flask import Flask, jsonify
from routes.estoque_routes import estoque_bp
from marshmallow.exceptions import ValidationError

app = Flask(__name__)
app.register_blueprint(estoque_bp)

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'message': error.messages})
