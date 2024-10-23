#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# create a venv
uv venv

# install project with dependencies (in editable mode for development)
uv pip install -e .
