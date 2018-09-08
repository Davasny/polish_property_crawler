FROM python:3.6-alpine

WORKDIR /usr/local/polish_property_crawler

RUN apk --no-cache add --virtual build-dependencies \
      build-base \
      py-mysqldb \
      gcc \
      libc-dev \
      libffi-dev \
      mariadb-dev \
      git
RUN apk add mariadb-dev

ADD https://api.github.com/repos/Davasny/polish_property_crawler/git/refs/heads/master /tmp/version.json

RUN git clone https://github.com/Davasny/polish_property_crawler.git ./

RUN pip install -r requirements.txt

RUN rm -rf .cache/pip \
    && apk del build-dependencies

COPY config.py ./

CMD python /usr/local/polish_property_crawler/app.py
