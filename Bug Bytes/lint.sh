#!/bin/bash
set -e

echo "Running black..."
black .

echo "Running isort..."
isort .

echo "Running ruff..."
ruff check . --fix

echo "Running mypy..."
PYTHONPATH=shop_drf mypy .
