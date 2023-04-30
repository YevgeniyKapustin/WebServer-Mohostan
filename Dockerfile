FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD chmod a+x scripts/*sh scripts/run_migration.sh scripts/run_gunicorn.sh
