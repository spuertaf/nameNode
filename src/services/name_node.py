from ..utils.index_table import IndexTable
from .grpc_service import GrpcService
from.http_api import HttpApiService


class NameNodeService:
    def __init__(
        self,
        data_nodes_table: IndexTable,
    ) -> None:
        self.__data_nodes_table = data_nodes_table
        self.grpc_gateway = GrpcService(self.__data_nodes_table)
        self.http_gateway = HttpApiService(self.__data_nodes_table)

            
    def init_http_service(self):
        self.http_gateway.build()
        
    
    def init_grpc_service(self):
        self.grpc_gateway.build()
    
    
    def build(self):
        self.init_grpc_service()
        self.init_http_service()
    
    
    
    