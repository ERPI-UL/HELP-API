FROM python:3.10

ENV IN_DOCKER=1 \
    PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

RUN apt-get update && apt-get install -y netcat

#COPY app/pyproject.toml app/poetry.lock /opt/app/

#RUN curl -sSL https://install.python-poetry.org | python3 -
#ENV PATH="${PATH}:/root/.local/bin"
#RUN poetry config virtualenvs.create false
COPY app /opt/app/
WORKDIR /opt/app
#RUN poetry install $([ "$ENV" = "production" ] && echo "--no-dev") --no-interaction
RUN pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh

EXPOSE 5000
RUN ["chmod", "+x", "/opt/app/docker-entrypoint.sh"]