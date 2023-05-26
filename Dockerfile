# Не предназначен для запуска без базы данных
FROM python:3.11.3

WORKDIR /app/

RUN pip install 'poetry==1.0.0'
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi --no-dev

COPY . .

CMD chmod a+x scripts/*sh &&  \
    /app/scripts/run_migration.sh &&  \
    /app/scripts/run_gunicorn.sh
