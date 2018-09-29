#!/bin/bash
set -e
find control_repository -name "*.py" | xargs mypy --ignore-missing-imports --strict --disallow-untyped-defs --disallow-untyped-calls --disallow-incomplete-defs
