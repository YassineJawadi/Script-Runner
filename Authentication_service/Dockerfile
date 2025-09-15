# Dockerfile
FROM python:3.13
COPY requirements.txt /userapp/requirements.txt
WORKDIR /userapp
RUN pip install -r requirements.txt --no-deps
COPY . /userapp
ENTRYPOINT ["python"]
CMD ["run.py"]