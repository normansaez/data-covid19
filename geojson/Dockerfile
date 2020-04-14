FROM python:3.7

ENV PYTHONUNBUFFERED 1

#### Install GEOS ####
# Inspired by: https://hub.docker.com/r/cactusbone/postgres-postgis-sfcgal/~/dockerfile/

#ENV GEOS http://download.osgeo.org/geos/geos-3.6.2.tar.bz2
#
#ADD $GEOS /install-postgis/
#WORKDIR /install-postgis/geos-3.6.2/
#
#RUN cd .. && tar jxvf geos-3.6.2.tar.bz2
##
#RUN ./configure --enable-python && make -j $(nproc) && make install
#RUN ldconfig
#RUN geos-config --cflags
RUN apt-get update && apt-get install -y vim bash npm # binutils libproj-dev gdal-bin vim bash npm
RUN npm install -g topojson
RUN npm install -g geojson

WORKDIR /app
#Prepare imports
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w","10", "-b", "0.0.0.0:5000", "--log-level", "INFO", "--timeout", "900", "app:app"]

