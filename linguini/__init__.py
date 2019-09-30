import os

from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from linguini.auth import login_manager
    login_manager.init_app(app)

    from linguini.database import db_session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    @app.before_request
    def check_route_access():
        if 'static/' in request.path or current_user.is_authenticated or request.endpoint is None:
            return  # Access granted
        if getattr(app.view_functions[request.endpoint], 'is_public', False):
            return # Access granted
        return login_manager.unauthorized()

    return app
