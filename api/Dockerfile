FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-2023-05-01

ENV IN_DOCKER=1 \
    PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    TZ="Europe/Paris"

RUN apt-get update && apt-get install -y netcat

COPY app /opt/app/
COPY requirements.txt /opt/
COPY docker-entrypoint.sh /opt/
WORKDIR /opt/

RUN pip install -r requirements.txt

EXPOSE 5000
RUN ["chmod", "+x", "/opt/docker-entrypoint.sh"]

ENTRYPOINT ["sh", "/opt/docker-entrypoint.sh"]