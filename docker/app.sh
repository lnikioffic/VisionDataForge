#!/bin/sh

nvidia-smi

alembic upgrade head

mkdir certs && cd certs && openssl genrsa -out jwt-private.pem 2048 && \
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

cd ..

python3 filling_db.py

uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4