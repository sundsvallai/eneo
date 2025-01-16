# Development

## Requirements

* Python >=3.10
* Docker

### Additional requirements

Additionally, in order to be able to use the platform to the fullest, install `libmagic` and `ffmpeg`.

```bash
sudo apt-get install libmagic1
sudo apt-get install ffmpeg
```

## Setup steps: Backend

To run the backend for this project locally, follow these steps:

1. Install poetry. This can be done by following the instructions on https://python-poetry.org/docs/.
2. Navigate to the backend directory in your terminal.
3. Run `poetry install` to install all dependencies into the current environment.
4. Copy .env.template to a .env, and fill in the required values. The required values can be found in `backend/README.md`.
5. Run `docker compose up -d` to start the required dependencies.
6. Run `poetry run python init_db.py` to run the migrations and setup the environment.
7. Run `poetry run start` to start the project for development.
8. (Optional) Run `poetry run arq src.instorage.worker.worker.WorkerSettings` to start the worker.

## Setup steps: Frontend

To run the frontend for this project locally, follow these steps:

1. Install node >= v20 (https://nodejs.org/en)
2. Install pnpm 8.9.0 (https://pnpm.io/)
3. Navigate to the frontend directory in your terminal
4. Run `pnpm run setup`
5. Navigate to `frontend/apps/web` and setup the .env file using the .env.example. You can learn more about the environment variables in `frontend/apps/web/README.md`
6. Run `pnpm -w run dev` to start the project for development.
7. Navigate to `localhost:3000` and login with email `user@example.com` and password `Password1!` (provided you have run the setup steps for the backend).

## Using Devcontainer for Development

The project is configured to use a devcontainer, which allows you to develop in a consistent environment using Visual Studio Code and Docker. Follow these steps to get started:

1. **Install Prerequisites**:
   - Ensure you have Docker installed on your machine.
   - Install Visual Studio Code and the Remote - Containers extension.

2. **Copy Environment Files**:
   - Before starting development, you need to set up your environment files:
     ```bash
     # In the backend directory
     cp .env.template .env

     # In the frontend/apps/web directory
     cp .env.example .env
     ```
   - Remember to update these .env files with appropriate values.

3. **Open the Project in a Devcontainer**:
   - Open the project folder in Visual Studio Code.
   - When prompted, or by clicking on the green icon in the bottom-left corner, select "Reopen in Container".
   - This will build the devcontainer as defined in `.devcontainer/devcontainer.json` and `.devcontainer/docker-compose.yml`.

4. **Accessing Services**:
   - The devcontainer setup will automatically forward ports 3000 and 8123, allowing you to access the frontend and any other services running on these ports.

5. **Post-Create Commands**:
   - After the container is created, the `postCreateCommand` specified in `.devcontainer/devcontainer.json` will run, setting up the environment.

6. **Developing**:
   - You can now develop as usual within the container. The environment will have all necessary dependencies installed and configured.

   **Important Notes**:
   - Database migrations are not run automatically. After the container is created, you'll need to run:
     ```bash
     cd backend
     poetry run python init_db.py
     ```
   - You'll need to manually start both the backend and frontend services in separate terminal windows:

     For the backend:
     ```bash
     cd backend
     poetry run start
     ```

     For the frontend:
     ```bash
     cd frontend
     pnpm run dev
     ```

     Running the frontend and backend in separate terminal windows gives you better control over each service's lifecycle. This makes it easier to restart individual services when needed, such as after installing new dependencies or when troubleshooting issues.

7. **Stopping the Devcontainer**:
   - To stop the devcontainer, simply close Visual Studio Code or use the "Remote - Containers: Reopen Folder Locally" command.

This setup ensures that all developers work in the same environment, reducing "it works on my machine" issues.

## Contribution guidelines

Coming soon.


## Architecture of each feature

The architecture for each feature strives to look like this:

```
feature_x/
├── api/
│   ├── feature_x_models.py
│   ├── feature_x_assembler.py
│   └── feature_x_router.py
├── feature_x.py
├── feature_x_repo.py
├── feature_x_service.py
└── feature_x_factory.py
```

An example of this can be seen in the `Spaces` feature.

### Function of each module

#### feature_x.py

The main class, the main domain object. Domain logic pertaining to how the feature works should live here.

#### feature_x_repo.py

Dependency inversion of database dependency. Should input a `Feature_x` class (or an `id`) and return that same class.

#### feature_x_service.py

Responsible for connecting this domain object with other related ones.

#### feature_x_factory.py

Factory class. Creates the domain object.

#### feature_x_router.py

Specifies the endpoints.

#### feature_x_models.py

Definition of the API schema.

#### feature_x_assembler.py

Translates domain objects to the API schema, allowing for the schema to change without affecting the shape of the domain object.

### Dependency injection

We use a [dependency injection framework](https://python-dependency-injector.ets-labs.org/index.html) to handle dependency injection for us. This framework creates all the other necessary classes, and handles their inter-dependency. This is typically done in the router.

### Connecting it together

Add the router [in the main router](https://github.com/inooLabs/intric-release/blob/main/backend/src/instorage/server/routers/__init__.py) in order to connect the endpoints to the application.

### Final considerations

While this is what we are striving towards at the moment, this is always subject to change.

## Migrations

We use [alembic](https://alembic.sqlalchemy.org/en/latest/) for our database migrations.
