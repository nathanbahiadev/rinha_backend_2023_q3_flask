# !bin/bash

flask db upgrade
gunicorn --bind 0.0.0.0:8000 --workers=4 --thread=8 "main:create_app()"
