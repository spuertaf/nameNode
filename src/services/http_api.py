from ..utils.index_table import IndexTable
from typing import Union
import os
from ..utils import env_vars 

from flask import Flask, Response, request
from pandas.core.frame import DataFrame

class HttpApiService:
    def __init__(
        self,
        data_nodes_table: IndexTable, 
        name:str = "http"
    ):
        self.name = name
        self.__data_nodes_table: IndexTable = data_nodes_table
        self.__service = Flask(self.name)
        self.__request: Union[None, dict]  = None
        self.__previous_position_given:int = 0 #ultima posicion de la lista de data nodes dada
        
    
    def validate_request(self) -> None:
        @self.__service.before_request
        def check_request_json():
            json_request:dict = request.get_json()
            #TODO Logging de peticion request.path.upper(), necesito IP
            assert json_request["payload"], f'Expected {{"payload": ...}} got {json_request}'
            self.__request = json_request
            #### TODO mirar como mejorar esto con 2 funciones!
            self.__data_nodes_table._get_gs_index()
            
    
    def act_on_error(self, response: Response) -> None:
        @self.__service.errorhandler(Exception)
        def handle_exceptions(error):
            response.data = str(error)
            response.status = int(os.environ["ERROR-status"])
            return response
    
        
    def handle_put(self, response: Response):
        @self.__service.route("/put", methods=["PUT"])
        def __round_robin_data_nodes():
            index_table: DataFrame = self.__data_nodes_table.get_data_nodes()
            avaiable_data_nodes = index_table["DataNodeIP"].unique()
            avaible_data_node:str = avaiable_data_nodes[self.__previous_position_given]
            if self.__previous_position_given + 1 >= len(avaiable_data_nodes):
                self.__previous_position_given = 0
            else:
                self.__previous_position_given +=1
            ###TODO Mirar repeticion
            response.data = avaible_data_node
            response.status = 200
            ####
            return response
        
        
    def handle_get(self, response: Response):
        @self.__service.route("/get", methods=["GET"])
        def __get_file_path():
            file_name = self.__request["payload"]
            node_with_file:list[list[str,str]] = self.__data_nodes_table.search_file(file_name)
            ###TODO Mirar repeticion
            response.data = str(node_with_file)
            response.status = 200
            ####
            return response
         
        
    def handle_search(self, response: Response):
        @self.__service.route("/search", methods=["GET"])
        def __search_regex():
            regex:str = self.__request["payload"]
            nodes_with_file:list[list[str,str]] = self.__data_nodes_table.search_file(regex)
            ###TODO Mirar repeticion
            response.data = str(nodes_with_file)
            response.status = 200
            ####
            return response

    
    def handle_list(self, response: Response):
        @self.__service.route("/list", methods=["GET"])
        def __list_files():
            regex:str = '.*'
            nodes_with_file:list[list[str,str]] = self.__data_nodes_table.search_file(regex)
            ###TODO Mirar repeticion
            response.data = str(nodes_with_file)
            response.status = 200
            ####
            return response
    
    
    def build(
        self, 
        response: Response, 
        host:str = os.environ["HTTP_HOST"], 
        port:int = os.environ["HTTP_PORT"]
    ):
        self.validate_request()
        self.act_on_error(response)
        self.handle_get(response)
        self.handle_search(response)
        self.handle_list(response)
        self.handle_put(response)
        self.__service.run(
            host = host, 
            port= port,
            threaded = True
        ) 
       
        
if __name__ == "__main__":
    data_nodes_table = IndexTable()
    service = HttpApiService(data_nodes_table)
    response = Response()
    service.build(response)

    
        