#!/bin/sh

export JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(64))')

python database/create_tables.py
flask run --host=0.0.0.0 --port=5000
