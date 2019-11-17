# For details on Makefiles, see the section notes.

# pytest unit testing options
PYTEST_UNIT_OPTS = -vv tests

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: test-unit

test-unit:
	@echo "+ $@"
	pytest ${PYTEST_UNIT_OPTS}