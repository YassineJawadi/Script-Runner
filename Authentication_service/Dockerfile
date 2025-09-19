# Dockerfile for Python microservice
FROM python:3.13-slim

# Set environment variables to avoid Python buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /userapp


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .


ENTRYPOINT ["python"]
CMD ["run.py"]
