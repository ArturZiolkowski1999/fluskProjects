from functools import wraps
from flask import abort
from flask_login import current_user

from ..api.errors import forbidden
from ..models.models import Permission


def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(perm):
                return forbidden('Has no permission')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
