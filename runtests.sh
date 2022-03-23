#!/bin/bash

. ./init-venv.sh

tests="*_test.py"

if [ -n "${1}" ]; then
  tests=$1
fi

python -m unittest discover -s tests -p $tests
