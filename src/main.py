from flask import Flask

from configs.database import init_db
from app.views import person_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(person_bp)
    init_db()
    return app
