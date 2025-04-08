FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

CMD ["sh", "-c", "python database/create_tables.py && flask run --host=0.0.0.0 --port=5000"]