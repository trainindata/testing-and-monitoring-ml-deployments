# For details on Makefiles, see the section notes.

# pytest unit testing options
PYTEST_UNIT_OPTS = -vv tests

TRAIN_MODEL_OPTS = gradient_boosting_model/train_pipeline.py

# Specify phony list to ensure make recipes do not conflict with real file names
.PHONY: test-unit train-model

train-model:
	@echo "+ $@"
	PYTHONPATH=. python ${TRAIN_MODEL_OPTS}

# test-unit depends on train-model
test-unit: train-model
	@echo "+ $@"
	pytest ${PYTEST_UNIT_OPTS}
