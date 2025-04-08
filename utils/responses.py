from flask import jsonify

def response(data=None, message=None, status=200):
    payload = {}
    if data is not None:
        payload["data"] = data
    if message is not None:
        payload["message"] = message
    return jsonify(payload), status