from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    else:
        app.config.update(test_config)
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    db.init_app(app)
    CORS(app)

    from .routes import api
    app.register_blueprint(api)

    # Auto-create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
