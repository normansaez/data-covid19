FROM httpd
EXPOSE 5001
RUN apt-get update
RUN apt-get install vim lynx less -y
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY users.conf /usr/local/apache2/conf/users.conf
RUN apachectl status
RUN apachectl restart

