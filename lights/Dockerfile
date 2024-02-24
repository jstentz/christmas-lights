FROM python:3.10.0-alpine

COPY lights/requirements.txt /

RUN pip install -r /requirements.txt

COPY . /lights

RUN pip install -e /lights

WORKDIR /lights/lights