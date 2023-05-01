FROM python:3.10

WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD chmod a+x scripts/*sh; /app/scripts/run_migration.sh; /app/scripts/run_gunicorn.sh
