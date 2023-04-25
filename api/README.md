# INDICO API

## Description 
L'API REST d'Indico permet de gérer les utilisateurs, les activités, les machines et toutes les ressource associées.

## Technologies
<div align="center">
  <img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png">
  <!-- fast api logo -->
    <img height="50" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png">
    <!-- postgres logo -->
    <img height="50" src="https://www.postgresql.org/media/img/about/press/elephant.png">
    <!-- tortoise orm logo -->
    <img height="50" src="https://tortoise.github.io/_static/tortoise.png">
    <img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/docker/docker.png">
</div>

## Configuration
- `DB_HOST` 
- `DATABASE` define the type of database. If the value equals 'postgres', it runs a test at start to check if th DB is alive
- `ENV` define the environment. Possible value are : "production", "development" or "test"
- `SECRET_KEY` should be set at a random value
