from ..utils.index_table import IndexTable
from .grpc_service import GrpcService
from.http_api import HttpApiService
import multiprocessing

from flask import Response

class NameNodeService:
    def __init__(
        self,
        data_nodes_table: IndexTable,
    ) -> None:
        self.__data_nodes_table = data_nodes_table
        self.grpc_gateway = GrpcService(self.__data_nodes_table)
        self.http_gateway = HttpApiService(self.__data_nodes_table)

            
    def init_http_service(self, response: Response) -> None:
        self.http_gateway.build(response)
        
    
    def init_grpc_service(self, grpc_listening_port:str) -> None:
        self.grpc_gateway.build(grpc_listening_port)
    
    
    def build(
        self, 
        grpc_listening_port:str, 
        response: Response
    ) -> None:
        http_process = multiprocessing.Process(target=self.init_http_service, args=(response,))
        http_process.start()
        self.init_grpc_service(grpc_listening_port)
    
    
    
    