import os
from flask import Flask


def create_app(test_config=None):
    from src.extensions import db, migrate, jwt, flask_bcrypt, ma
    from src.models.Post import Post
    from src.models.Roles import Role
    from src.models.User import User

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("src.repository.config.Config")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from src.controller.cli import register_comands

    register_comands(app)
    from src.controller.routes import user, roles, post, error
    from src.controller import auth

    error.register_error_handlers(app)
    app.register_blueprint(auth.app)
    app.register_blueprint(user.app)
    app.register_blueprint(roles.app)
    app.register_blueprint(post.app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    ma.init_app(app)

    return app
