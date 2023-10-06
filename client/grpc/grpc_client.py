from .contracts import nameNode_pb2_grpc, nameNode_pb2

import grpc

grpc_connection = grpc.insecure_channel("3.94.130.231:50000")
grpc_channel = nameNode_pb2_grpc.Add2IndexStub(grpc_connection) 
request = nameNode_pb2.add2IndexRequest(dataNodeIP="DataNode1", path2Add="path/to/txt/file.txt")
response = grpc_channel.add_2_index(request)
print(response)
                                        