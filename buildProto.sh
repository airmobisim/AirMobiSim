#!/bin/zsh


cd proto
protoc airmobisim.proto --cpp_out=../airmobisimVeins/subprojects/veins_libairmobisim2/src/veins_libairmobisim/proto --grpc_out=../airmobisimVeins/subprojects/veins_libairmobisim2/src/veins_libairmobisim/proto  --plugin=protoc-gen-grpc=`which grpc_cpp_plugin`
cd ../

python -m grpc_tools.protoc --python_out=. --grpc_python_out=. proto/airmobisim.proto -I .
