FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY . .

RUN .venv/bin/pip install -e .

CMD [".venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "-m", "007", "mirrdash.wsgi:app"]
