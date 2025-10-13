FROM python:3.11-slim

WORKDIR /app

# system deps if required (none for now)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.main

# run with gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:create_app()", "--workers", "4", "--threads", "2"]
