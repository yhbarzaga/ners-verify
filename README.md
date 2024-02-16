# NERS powered by [Verify](https://www.veryfi.com/)
Welcome to the Non-business Expenses Report System, your microservice for track expenses not related to commercial transactions.

Below will be detailed steps to have the local environment setup or trough docker.


# Setup environment

## Requirements
Initial system requirements
* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Install dependencies
By default, the dependencies are managed with `Poetry`([installation instructions](https://python-poetry.org/docs/#installation)).

From the root directory you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Next, open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc. 

> [!IMPORTANT]  
> Make sure your editor uses the environment you just created with Poetry.

---

# Local development
* The stack used for develop the services:
  - api: FastAPI.
  - database: PostgreSQL object-relational database system.
  - proxy: A reverse proxy and load balancer for HTTP and TCP-based applications with Traefik.

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

Now you can open your browser and interact with these URLs:
  - Automatic interactive documentation with Swagger UI (from the OpenAPI NERS Api): http://localhost/docs
  - Alternative automatic documentation with ReDoc (from the OpenAPI NERS Api): http://localhost/redoc
  - Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs api
```
---
## Authentication

Endpoints are behind authentication, so in order to successfully request you need to provide an API KEY in the request header in form of `Bearer token`.
For the purpose of simplicity the API KEY is any UUID, as long as follows the expected format will be valid.

e.g.
```
curl -X 'GET' \
  'http://localhost/api/v1/staff/<staff_id>/refund' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer d344f870-0843-4fd0-9f63-f1bc77d99c60'
```

On the swagger page will be available a button for Authorization, click on it for set a global API KEY that will be used across all endpoints.

---
## Testing

If your stack is already up and running you just want to run the tests, you can use:

```bash
docker-compose exec -T api make test
```

> [!IMPORTANT]  
> If you are not in detach mode while execute the docker-compose execute this command in a separate terminal.

---
### Migrations

Alembic is the database migration tool used for the application.
As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

* Start an interactive session in the api container:

```console
$ docker-compose exec api bash
```

If you created a new model in `./app/models/`, make sure to import it in `./app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic. 
Any update to existent models will be automatically recognize by alembic.

* After changing a model, inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```
