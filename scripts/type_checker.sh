#!/bin/bash
set -e
find control_repository -name "*.py" | xargs mypy --ignore-missing-imports
