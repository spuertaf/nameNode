from typing import Union
import os
import re

import pandas as pd

class IndexTable:
    _data_nodes_index: Union[None, pd.DataFrame] = None
    
    def __init__(cls):
        if cls._data_nodes_index is None:
            cls.__get_gs_index()
    
    
    def __get_gs_index(cls):
        cls._data_nodes_index = pd.read_csv(
            os.environ["PATH_2_GS_INDEX"], 
            index_col=None
        )
    
    
    def __append_2_table(
        cls,
        row_2_append: list[str, str]
        ) -> None:
        row = pd.DataFrame(
            data = [row_2_append],
            columns = ['DataNodeIP', 'Path2File']
        )
        
        cls._data_nodes_index: pd.DataFrame = pd.concat(
            [cls._data_nodes_index, row],
            axis = 0
        )
    
    
    def __update_gs_index(cls) -> None:
        cls._data_nodes_index.to_csv(
            os.environ["PATH_2_GS_INDEX"], 
            index=False
        )
        
        
    def update_table(
        cls,
        row_2_append:list[str,str]
    ):
        cls.__get_gs_index()
        cls.__append_2_table(row_2_append)
        cls.__update_gs_index()
        
    
    def search_file(cls, file_name:str) -> list[list[str,str]]:
        regex_pattern = fr"{file_name}"
        nodes_with_file:pd.DataFrame = cls._data_nodes_index[
            cls._data_nodes_index['Path2File'].str.contains(
                regex_pattern, 
                flags=re.IGNORECASE
            )
        ]
        return nodes_with_file.values.tolist()
    
    
if __name__ == "__main__":
       
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Admin\\Downloads\\practical-case-331501-6ad949ef28a5.json"
    os.environ["PATH_2_GS_INDEX"] = "gs://data-nodes-index/index.csv"    
     
    index = IndexTable()
    #index.update_table(["NameNode1","/mount/customers.csv"])
    #index.update_table(["NameNode2","/mount/dir/customers.csv"])
    print(index.search_file('pandas.csv'))