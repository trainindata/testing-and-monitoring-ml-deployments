# For details on Makefiles, see the section notes.

# pytest integration testing options
PYTEST_INTEGRATION_OPTS = -vv -m integration tests

# pytest differential testing options
PYTEST_DIFFERENTIAL_OPTS = -vv -m differential tests

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-local test-integration

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
