FROM python:3.7

RUN wget http://nginx.org/keys/nginx_signing.key
RUN apt-get update
RUN apt-key add nginx_signing.key
RUN apt install -y nginx
RUN apt-get install -y vim less bash

RUN unlink /etc/nginx/sites-enabled/default
COPY reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY htpasswd /etc/nginx/htpasswd
RUN ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/
RUN service nginx configtest
RUN service nginx restart

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
