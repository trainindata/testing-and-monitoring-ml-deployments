FROM python:3.9.5-slim-buster

RUN mkdir -p /opt/app
COPY requirements /opt/app/requirements
RUN pip install --upgrade pip

# ensure we can run the make commands
RUN apt-get update -y && \
 	apt-get install -y make && \
 	apt-get install -y libffi-dev gcc && \
 	# for swagger
 	apt-get install -y curl && \
 	# for postgres driver
 	apt-get install -y libpq-dev

RUN pip install -r /opt/app/requirements/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/"

ADD . /opt/app
WORKDIR /opt/app
