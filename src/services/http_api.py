from ..utils.index_table import IndexTable
from typing import Union
import os
from ..utils import env_vars 

from flask import Flask, Response, request
from pandas.core.frame import DataFrame
import numpy as np

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
        self.__previous_position_given_put:int = 0 #ultima posicion de la lista de data nodes dada
        self.__previous_position_given_get:int = 0
        self.__previous_file_searched = None
        
    
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
            print(error)
            response.data = str(error)
            response.status = int(os.environ["ERROR-status"])
            return response
    

    def __round_robin_data_nodes(
            self,
            previous_position_given:int, 
            avaible_data_nodes:list[str]
    ) -> tuple[int, str]:
        avaible_data_node:str = avaible_data_nodes[previous_position_given]
        if previous_position_given + 1 >= len(avaible_data_nodes):
            previous_position_given = 0
        else:
            previous_position_given += 1
        return (previous_position_given, avaible_data_node,) 

        
    def handle_put(self, response: Response):
        @self.__service.route("/put", methods=["PUT"])
        def __put_in_2_data_node():
            index_table: DataFrame = self.__data_nodes_table.get_data_nodes()
            avaiable_data_nodes = index_table["DataNodeIP"].unique()
            self.__previous_position_given_put, response.data = self.__round_robin_data_nodes(
                self.__previous_position_given_put,
                avaiable_data_nodes
            )
            ###TODO Mirar repeticion
            response.status = 200
            ####
            return response
        
        
    def handle_get(self, response: Response):
        @self.__service.route("/get", methods=["GET"])
        def __get_file_path():
            file_name = self.__request["payload"]
            self.__previous_file_searched = file_name
            if self.__previous_file_searched != file_name:
                self.__previous_position_given_get = 0
            nodes_with_file:list[list[str,str]] = self.__data_nodes_table.search_file(file_name)
            print(nodes_with_file)
            nodes_ips: list[str] = list(map(lambda x: x[0], nodes_with_file))
            print(nodes_ips)
            print(self.__previous_position_given_get)
            self.__previous_position_given_get, available_data_node = self.__round_robin_data_nodes(
                self.__previous_position_given_get,
                nodes_ips
            )
            print(self.__previous_position_given_get)
            available_data_node = list(filter(lambda x: x[0] == available_data_node, nodes_with_file))
            if len(available_data_node) > 1:
                raise Exception("More than one data node to respond not supported")

            ###TODO Mirar repeticion
            response.data = str(available_data_node)
            response.status = 200
            ###
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

    
        