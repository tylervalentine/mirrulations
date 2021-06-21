FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv
RUN .venv/bin/pip install flask flask-cors redis gunicorn

COPY . .

CMD [".venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "-m", "007", "wsgi:app"]
