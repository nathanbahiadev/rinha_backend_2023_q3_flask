# !bin/bash

gunicorn --bind 0.0.0.0:8000 --worker-connections=20000 --workers=4 --threads=8 "main:create_app()"
