### 1. Get Linux
FROM alpine:3.7

WORKDIR /app

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache vim
#&& apk add --no-cache openjdk8-jre

### 3. Get Python, PIP

RUN apk add --no-cache python3 \
&& apk add --update curl gcc g++ \
&& apk add python3-dev \
&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

#Prepare imports
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#Prepare environment

################################################################
#XXX: Remove this when we have an service account to download it
#     also we should unremove the last line in prepare_env.py
################################################################

#### OPTIONAL : 4. SET JAVA_HOME environment variable, uncomment the line below if you need it

#ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

####

EXPOSE 5004
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5004", "--log-level", "INFO", "--timeout", "900", "app:app"]
