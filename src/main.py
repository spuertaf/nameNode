from .utils import env_vars
from .utils.index_table import IndexTable
from .services.name_node import NameNodeService
import os 

from flask import Response

data_nodes_table = IndexTable()
name_node = NameNodeService(data_nodes_table)
response = Response()
name_node.build(os.environ["GRPC_PORT"],response)