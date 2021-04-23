# Demo project for processing datasets from airline survey datasets

## Requirements
    1. `docker` installed locally.

## How to run
    * `docker-compose -f docker-compose.yml up --scale worker=2 --build`

## Libraries
    1. `mongoengine`
    2. `fastapi`
    3. `celery`
    4. `redis`
    5. `pydantic`

## DB
    * Utilizes MongoDB for `docker-compose`

## About the project
    1. You can upload dataset file/files via the API.
    2. Those records are sent to Celery for background processing as the broker (Redis is the messaging queue).
    3. Records are then parsed and added to the DB (customer_id being the identifier)
    4. Records are returned in Yaml format and can be downloaded.
    5. A few queries are in place for specific fields (can be added to)
    6. A task ID is sent back when file is uploaded, and the ID can be used to get the status of the job.
