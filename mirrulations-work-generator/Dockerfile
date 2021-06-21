FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY . .

RUN .venv/bin/pip install -e .

CMD [".venv/bin/python", "src/mirrgen/work_generator.py"]
