#!/bin/bash

# Coverage
coverage run --source=src -m pytest
coverage report
coverage xml
genbadge coverage -i ./coverage.xml

# Linter
flake8 src --statistics --output-file flake8stats.txt --exit-zero
genbadge flake8 -i ./flake8stats.txt

# Cleanup
rm ./coverage.xml
rm ./flake8stats.txt

echo "==="
echo "Execution finished, reports deleted"
echo "==="
