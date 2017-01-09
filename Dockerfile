FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
ENV POSTGRES_HOST "db"
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/base.txt
VOLUME /code
