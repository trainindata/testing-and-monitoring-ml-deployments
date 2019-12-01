# For details on Makefiles, see the section notes.

# pytest integration test options
PYTEST_INTEGRATION_OPTS = -vv tests

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: run-service-local integration-tests

# start up Flask API service
run-service-development:
	@echo "+ $@"
	python run.py


integration-tests:
	@echo "+ $@"
	pytest ${PYTEST_UNIT_OPTS}