#!/bin/bash

# To install requirements:
# pip install tox pytest pytest-pep8 pytest-cov

py.test --ignore=build --pep8 -v --cov=mongosql --cov-report=term-missing mongosql "$@"
