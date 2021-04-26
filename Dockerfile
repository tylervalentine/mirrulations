FROM python:3.8-slim-buster

WORKDIR /app

COPY src/c21client/client.py .

RUN python3 -m venv .venv
RUN .venv/bin/pip install requests python-dotenv

CMD [".venv/bin/python", "client.py"]