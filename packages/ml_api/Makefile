# For details on Makefiles, see the section notes.
NAME=ml_api
VERSION=$(shell git rev-parse HEAD)
REPO=christophergs

# pytest integration testing options
PYTEST_INTEGRATION_OPTS = -vv -m integration tests

# pytest differential testing options
PYTEST_DIFFERENTIAL_OPTS = -vv -m differential tests

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-local test-integration tag-push-master tag-push-local db-migrations

tag-push-local:
	@echo "+ $@"
	env TARGET=$(VERSION) docker-compose -f docker/docker-compose-ci-candidate.yml build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
	docker push $(REPO)/$(NAME):$(VERSION)

tag-push-master:
	@echo "+ $@"
	env TARGET=master docker-compose -f docker/docker-compose-ci-master.yml build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
	docker push $(REPO)/$(NAME):master

# start up Flask API service
run-service-development:
	@echo "+ $@"
	python run.py

test-integration:
	@echo "+ $@"
	PYTHONPATH=. pytest ${PYTEST_INTEGRATION_OPTS}

test-differential: test-integration
	@echo "+ $@"
	PYTHONPATH=. pytest ${PYTEST_DIFFERENTIAL_OPTS}

db-migrations:
	@echo "+ $@"
	alembic -c alembic.ini upgrade head
