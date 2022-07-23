# pull official base image
FROM python:3.9.5-alpine

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk upgrade && apk add postgresql-dev gcc python3-dev musl-dev && \
    apk add zlib zlib-dev linux-headers python3-dev libffi-dev && \
    pip3 install --upgrade pip setuptools && \
    rm -rf /var/cache/apk || rm -rf /etc/apk/cache || echo "clean cache is failed"
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh

# copy project
COPY ./src/ /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
