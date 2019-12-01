# For details on Makefiles, see the section notes.

# pytest unit testing options
PYTEST_INTEGRATION_OPTS = -vv -m integration tests

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-local test-integration

# start up Flask API service
run-service-development:
	@echo "+ $@"
	python run.py

test-integration:
	@echo "+ $@"
	PYTHONPATH=. pytest ${PYTEST_INTEGRATION_OPTS}
