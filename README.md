<div align="center">

![wordmark on dark blue](https://github.com/user-attachments/assets/67b9c7df-4fc7-4acb-9e54-8bdbd81ad9b9)

intric is an easy-to-use platform for building and using AI-powered assistants and tools. Take advantage of AI today instead of tomorrow.

[Local Development](#local-development) • [Contribution](#contribution-guidelines) **(coming soon)**

</div>

## Local development

Read below on how to setup the project for local development.

### Requirements

* Python >=3.10
* Docker

#### Additional requirements

Additionally, in order to be able to use the platform to the fullest, install `libmagic` and `ffmpeg`.

```
sudo apt-get install libmagic1
sudo apt-get install ffmpeg
```

### Setup steps: Backend

To run the backend for this project locally, follow these steps:

1. Install poetry. This can be done by following the instructions on https://python-poetry.org/docs/.
2. Navigate to the backend directory in your terminal.
3. Run `poetry install` to install all dependencies into the current environment.
4. Copy .env.template to a .env, and fill in the required values. The required values can be found in `backend/README.md`.
5. Run `docker compose up -d` to start the required dependencies.
6. Run `poetry run python init_db.py` to run the migrations and setup the environment.
7. Run `poetry run start` to start the project for development.
8. (Optional) Run `poetry run arq src.instorage.worker.worker.WorkerSettings` to start the worker.

### Setup steps: Frontend

To run the frontend for this project locally, follow these steps:

1. Install node >= v20 (https://nodejs.org/en)
2. Install pnpm 8.9.0 (https://pnpm.io/)
3. Navigate to the frontend directory in your terminal
4. Run `pnpm run setup`
5. Navigate to `frontend/apps/web` and setup the .env file using the .env.example. You can learn more about the environment variables in `frontend/apps/web/README.md`
6. Run `pnpm -w run dev` to start the project for development.
7. Navigate to `localhost:3000` and login with email `user@example.com` and password `Password1!` (provided you have run the setup steps for the backend).

## Contribution guidelines

Coming soon.


## Copyright Holders

The development of this project has been partially funded by the following entities, each holding specific copyright interests in parts of the code:

- **Sundsvalls Kommun**

The parts that each of the entities hold copyright to is marked within the respective files. For all code where there is no marking, the copyright should be attributed to **inooLabs**.

For any inquiries regarding usage rights, please contact jonatan.cerwall@inoolabs.com.