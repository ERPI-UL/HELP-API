# INDICO API

## Description 
APi qui permet de gerer les utilisateurs et de collecter les données et les scénarios pédagogiques.


## Configuration
- `DB_HOST` 
- `DATABASE` define the type of database. If the value equals 'postgres', it runs a test at start to check if th DB is alive
- `ENV` define the environment. Possible value are : "production", "development" or "test"
- `SECRET_KEY` should be set at a random value
