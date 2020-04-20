FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y vim bash

WORKDIR /app
#Prepare imports
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
EXPOSE 5003
#CMD ["gunicorn", "-w","5","-b", "0.0.0.0:5001", "--certfile", "/app/cert.pem", "--keyfile", "/app/key.pem", "--log-level", "INFO", "--timeout", "900", "app:app"]
CMD ["gunicorn", "-w","5","-b", "0.0.0.0:5003", "--log-level", "INFO", "--timeout", "900", "app:app"]

