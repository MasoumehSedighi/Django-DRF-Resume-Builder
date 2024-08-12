FROM python:3.11.9-alpine3.19

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt      /temp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /temp/requirements.txt


ENV PATH="/venv/bin:$PATH"
