from typing import Union
from ..utils.index_table import IndexTable
from concurrent import futures
from .configs.contracts import nameNode_pb2_grpc
from .configs.contracts.nameNode_pb2 import add2IndexRequest, add2IndexResponse
import os

from grpc._server import _Server as GrpcServer
import grpc


class GrpcService(nameNode_pb2_grpc.Add2IndexServicer):
    def __init__(self, data_nodes_table:IndexTable, name:str = "grpc"):
        self.__data_nodes_table:IndexTable = IndexTable()
        self.__service:GrpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
            
    def add_server_functions(self) -> None:
        #añadir las funcionalidades de la clase al servidor
        nameNode_pb2_grpc.add_Add2IndexServicer_to_server(GrpcService(self.__data_nodes_table), self.__service)
        
    
    def create_end_point(self, listening_port:str) -> None:
        self.__service.add_insecure_port(listening_port)
        
    
    def add_2_index(self, request: add2IndexRequest, context) -> add2IndexResponse:
        print(f"Nueva Solicitud recivida de {context.peer()}")
        status_code: Union[None, int] = None
        try:
            self.__data_nodes_table.update_table(
                [request.dataNodeIP, request.path2Add]
            )
            status_code = int(os.environ["OK-status"])
        except Exception as e:
            #logger excepcion
            print(str(e))
            status_code = int(os.environ["ERROR-status"])
        finally:
            return add2IndexResponse(statusCode=status_code)
    
    
    def build(self, listening_port:str):
        self.add_server_functions()
        self.create_end_point(listening_port)
        self.__service.start()
        print("Server started")
        self.__service.wait_for_termination()
        

if __name__ == "__main__":
    from ..utils import env_vars
    env_vars
    table = IndexTable()
    grpc_s = GrpcService(table)
    grpc_s.build(listening_port="[::]:80")
    