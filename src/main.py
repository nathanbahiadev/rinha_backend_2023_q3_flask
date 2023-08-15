from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware

from app.views import person_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(person_bp)
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, 
        profile_dir="./profiles",
        stream=None,
        filename_format='{elapsed:.0f}ms:::{method}.{path}:::{time:.0f}.prof'
    )
    return app
