FROM python:3.7
ENV APP /app
RUN mkdir $APP
WORKDIR $APP
EXPOSE 5000

RUN echo "Starting docker with flask"
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx vim bash
RUN pip3 install uwsgi
RUN curl https://sdk.cloud.google.com | bash

COPY requirements.txt .
RUN mkdir anticipables
RUN pip install -r requirements.txt
COPY nginx.conf /etc/nginx/sites-enabled/default
COPY . .
CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app
CMD [ "uwsgi", "--ini", "app.ini" ]

