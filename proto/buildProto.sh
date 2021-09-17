#!/bin/zsh
protoc airmobisim.proto --cpp_out=/Users/hardes/Documents/cms_git/airmobisimVeins/subprojects/veins_libairmobisim2/src/veins_libairmobisim/proto --grpc_out=/Users/hardes/Documents/cms_git/airmobisimVeins/subprojects/veins_libairmobisim2/src/veins_libairmobisim/proto --python_out=.   --plugin=protoc-gen-grpc=`which grpc_cpp_plugin`

protoc airmobisim.proto --grpc_out=.  --python_out=.  --plugin=protoc-gen-grpc=`which grpc_python_plugin`
