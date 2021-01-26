#!/bin/bash
set -eu

SCRIPT_DIR=$(
    cd $(dirname $0)
    pwd
)
BASE_DIR=$(
    cd ${SCRIPT_DIR}/../..
    pwd
)

flake8 ${BASE_DIR} \
    --exclude "${BASE_DIR}/tests/resources" \
    --count --show-source --statistics
