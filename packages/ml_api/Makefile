# For details on Makefiles, see the section notes.
NAME=ml_api
VERSION=$(shell git rev-parse HEAD)
REPO=UPDATEME
PASSWORD=UPDATEME

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-development tag-push-master tag-push-local db-migrations


tag-push-local:
	@echo "+ $@"
	docker login --username $(REPO) --password $(PASSWORD)
	env TARGET=$(VERSION) docker-compose -f docker/docker-compose-ci-candidate.yml build
	docker push $(REPO)/$(NAME):$(VERSION)

tag-push-master:
	@echo "+ $@"
	docker login --username $(REPO) --password $(PASSWORD)
	env TARGET=master docker-compose -f docker/docker-compose-ci-master.yml build
	docker push $(REPO)/$(NAME):master

# start up Flask API service
run-service-development:
	@echo "+ $@"
	python run.py

run-service-wsgi:
	@echo "+ $@"
	gunicorn --bind 0.0.0.0:5000 \
			 --workers=1 \
			 --log-config gunicorn_logging.conf \
             --log-level=DEBUG \
             --access-logfile=- \
             --error-logfile=- \
             run:application

db-migrations:
	@echo "+ $@"
	PYTHONPATH=. alembic -c alembic.ini upgrade head
