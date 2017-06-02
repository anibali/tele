#!/bin/bash

# Change into project directory
cd "$(dirname "${BASH_SOURCE[0]}")/../"

# Package and upload to PyPI
docker-compose run --rm tele python3 setup.py sdist upload
