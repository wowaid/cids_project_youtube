FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary

COPY src/load_data.py /app/load_data.py

CMD ["python", "/app/load_data.py"]