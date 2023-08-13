from flask import Flask

from configs.database import database
from configs.settings import Settings
from configs.migrations import migrate
from views import person_bp
from models import PersonModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    app.app_context().push()

    app.register_blueprint(person_bp)
    database.init_app(app)
    migrate.init_app(app, database)

    return app
