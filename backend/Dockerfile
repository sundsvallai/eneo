FROM python:3.11

# Install ffmpeg
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

# Install libmagic, for mimetypes
RUN apt-get install libmagic1

RUN pip install poetry

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock ./

COPY . /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD ["sh", "-c", "./run.sh"]
