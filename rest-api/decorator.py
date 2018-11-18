import time
import logging
from flask import jsonify
from functools import wraps
from flask import request

LOGGER = logging.getLogger(__name__)


def validate_form(form=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if form:
                vf = form(request.values)
                if not vf.validate():
                    return jsonify(error=vf.errors)
                start_time = time.clock()
                retval = f(form=vf, *args, **kwargs)
                elapsed_time = time.clock() - start_time
                LOGGER.debug("%s execution time: %s sec",
                             f.__name__, elapsed_time)
                return retval
            return f(*args, **kwargs)
        return decorated_function
    return decorator
