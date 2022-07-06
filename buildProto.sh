#!/bin/zsh
poetry run python -m grpc_tools.protoc --python_out=. --grpc_python_out=. proto/airmobisim.proto -I .
