FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update --fix-missing \
    && apt-get -y install libpq-dev python3-dev gcc \
    && pip install psycopg2

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.dev.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]