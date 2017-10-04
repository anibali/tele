#!/bin/bash

# Change into project directory
cd "$(dirname "${BASH_SOURCE[0]}")/../"

# Run tests
docker-compose run --rm tele python3 setup.py test
