# !bin/bash

gunicorn --bind 0.0.0.0:8000 --worker-connections=20000 --workers=2 --threads=4 "main:create_app()"
