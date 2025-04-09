from flask import request, jsonify
from functools import wraps
from services.user_service import get_user_by_token
from utils.responses import response

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_user_by_token(request)
            if user is None:
                return response(message={"erro": "Usuário não autenticado"}, status=401)
            if user.papel not in roles:
                return response(message={'erro': 'Permissão negada'}, status=403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

require_admin = require_role('admin')
