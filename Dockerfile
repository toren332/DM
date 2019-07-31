FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD /requirements /code/requirements/

RUN pip install -r requirements/all.txt

ADD . /code/