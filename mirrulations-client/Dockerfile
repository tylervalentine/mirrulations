FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY mirrulations-client .

RUN .venv/bin/pip install -e .

CMD [".venv/bin/python", "src/mirrclient/client.py"]