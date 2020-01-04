FROM python:3.7-alpine
WORKDIR /application

COPY ./requirements.txt requirements.txt
RUN apk add --no-cache \
		gcc \
		libc-dev \
		linux-headers \
		bash; \
	pip install -r requirements.txt;

COPY . /application


EXPOSE 5000
VOLUME /application
CMD gunicorn --workers=1 --bind 0.0.0.0:5000 application:application
