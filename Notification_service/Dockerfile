FROM python:3.11
COPY requirements.txt /notifapp/requirements.txt
WORKDIR /notifapp
RUN pip install --no-cache-dir -r requirements.txt --no-deps
COPY . /notifapp
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
EXPOSE 5002
ENTRYPOINT ["flask"]
CMD ["run"]
