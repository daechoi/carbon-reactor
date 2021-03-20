FROM python:3.9-alpine as basebuild

RUN apk add \
  python3-dev \
  vim \
  gcc \
  make \
  postgresql-dev \
  postgresql-libs \
  libressl-dev \
  libffi-dev \
  musl-dev

ENV PYTHONPATH /

FROM basebuild as python_build
COPY ./requirements.txt /data_import/requirements.txt
COPY ./.env.production /.env.production
RUN pip install -r /data_import/requirements.txt

ADD . /

WORKDIR /data_import

from python_build as data_run

CMD ["sh", "-c", "python3 tiblio.py"]
