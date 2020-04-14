FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y vim bash

WORKDIR /app
#Prepare imports
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "-b", "0.0.0.0:5001", "--log-level", "INFO", "--timeout", "900", "app:app"]

