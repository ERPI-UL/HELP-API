FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-2023-05-01

ENV IN_DOCKER=1 \
    PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    TZ="Europe/Paris"

RUN apt-get update && apt-get install -y netcat

COPY app /opt/app/
COPY requirements.txt /opt/
WORKDIR /opt/

RUN pip install -r requirements.txt

EXPOSE 5000

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD uvicorn app.main:app --port 5000 --host 0.0.0.0 --forwarded-allow-ips="*" --proxy-headers
