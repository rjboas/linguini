from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def public_route(decorated_function):
    """
    Makes decorated route accessible to logged-out users
    
    This check is performed in the __init__.check_route_access function
    """

    decorated_function.is_public = True
    return decorated_function


def has_role(roles):
    """Makes decorated route require user to have any of the required roles to access"""

    def decorator(decorated_function):

        @wraps(decorated_function)
        def wrapper(*args, **kwds):
            if current_user.role in roles:
                return decorated_function(*args, **kwds)
            flash('You do not have permission to perform this action.')
            return redirect(url_for('.index'))

        return wrapper

    return decorator


def in_pc(pc):
    """Makes decorated route require user to be in the required pc to access"""

    def decorator(decorated_function):

        @wraps(decorated_function)
        def wrapper(*args, **kwds):
            if current_user.pc == pc:
                return decorated_function(*args, **kwds)
            flash('You do not have permission to perform this action.')
            return redirect(url_for('.index'))

        return wrapper

    return decorator
