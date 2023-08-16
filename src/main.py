from flask import Flask

from app.views import person_bp
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@postgres:5432/mydatabase"
    app.url_map.strict_slashes = False
    app.register_blueprint(person_bp)
    
    db.init_app(app)

    return app
