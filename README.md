1. build protos:
```shell
python -m grpc_tools.protoc -I./protos --python_out=./service --pyi_out=./service --grpc_python_out=./service ./protos/api.proto
python -m grpc_tools.protoc -I./protos --python_out=./client --pyi_out=./client --grpc_python_out=./client ./protos/api.proto
```

2. run server:
```shell
python service/app.py
```

3. run client:
```shell
python client/client.py -url http://stackoverflow.com
python client/client.py -ret 0
```