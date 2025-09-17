FROM python:3.11
COPY requirements.txt /robotapp/requirements.txt
WORKDIR /robotapp
RUN pip install --no-cache-dir -r requirements.txt --no-deps
COPY . /robotapp
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
EXPOSE 5001
ENTRYPOINT ["flask"]
CMD ["run"]
