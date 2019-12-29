#!/bin/bash

set -euox pipefail

MODEL_VERSION="master"
MODEL_VARIANT="candidate"
NUMBER_OF_TESTS="50"

CANDIDATE_MODEL_SHA="$(git rev-parse HEAD)"

# required once only (or whenever you make local changes):
# comment these two lines out otherwise as they can take some time.
make tag-push-local

# should only be run once a model version has been finalized
# best practice is to run as part of a CI pipeline on merge to master branch.
make tag-push-master

## Pull latest published image
env TARGET=master docker-compose --file docker/docker-compose.yml pull

# start latest (master) image and local image
env TARGET=master SERVER_PORT=5000 docker-compose --project-name master --file docker/docker-compose-ci-master.yml up --no-recreate -d ml_api
env TARGET=$CANDIDATE_MODEL_SHA SERVER_PORT=5001 docker-compose --project-name head --file docker/docker-compose-ci-candidate.yml up --no-recreate -d ml_api

## Start the test runner containers
env TARGET=master docker-compose --project-name master --file docker/docker-compose-ci-master.yml run -d --name differential-tests-expected differential-tests sleep infinity
env TARGET=$CANDIDATE_MODEL_SHA docker-compose --project-name head --file docker/docker-compose-ci-candidate.yml run -d --name differential-tests-actual differential-tests sleep infinity

docker ps --all

echo "===== Running $CANDIDATE_MODEL_SHA ... ====="

## Compute the actual predictions (i.e. candidate model)
docker exec --user root differential-tests-actual \
    python3 differential_tests compute sample_payloads differential_tests/actual_results --base-url http://head_ml_api_1:5001

## Copy the actual predictions
docker cp differential-tests-actual:/opt/app/differential_tests/actual_results/. differential_tests/actual_results

echo "===== Running master ... ====="
## Compute the expected marginals (i.e. existing model)
docker exec --user root differential-tests-expected \
    python3 differential_tests compute sample_payloads differential_tests/expected_results --base-url http://master_ml_api_1:5000

## Copy the expected marginals
docker cp differential-tests-expected:/opt/app/differential_tests/expected_results/. differential_tests/expected_results

# then copy all results into the differential-tests-actual container for comparison
docker cp differential_tests/expected_results/. differential-tests-actual:/opt/app/differential_tests/expected_results

echo "===== Comparing $CANDIDATE_MODEL_SHA vs. master ... ====="
## Compare the expected and actual marginals
docker exec differential-tests-actual \
    python3 -m differential_tests compare differential_tests/expected_results differential_tests/actual_results

# clear any docker containers (will stop the script if no containers found)
docker rm $(docker ps -a -q) -f
