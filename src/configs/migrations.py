import os

from flask_migrate import Migrate

migrations_folder = os.path.join(os.path.dirname(__file__), "migrations")
migrate = Migrate(directory=migrations_folder)
