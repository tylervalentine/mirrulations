FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update; apt-get install docker.io -y
RUN python3 -m venv .venv

COPY mirrulations-dashboard .

RUN .venv/bin/pip install -e .

CMD [".venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "-m", "007", "mirrdash.wsgi:app"]
