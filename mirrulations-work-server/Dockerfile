FROM python:3.8-slim-buster

WORKDIR /app

COPY mirrulations-work-server .

RUN python3 -m venv .venv

RUN .venv/bin/pip install -e .

CMD [".venv/bin/gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "-m", "007", "mirrserver.wsgi:app"]