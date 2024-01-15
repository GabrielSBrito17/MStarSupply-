from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from models.models import db
from routes.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    app.register_blueprint(routes)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run()