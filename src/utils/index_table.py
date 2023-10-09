from typing import Union
import os
import re

from pandas.core.frame import DataFrame
import pandas as pd

class IndexTable:
    def __init__(self):
        self._data_nodes_index:Union[None, DataFrame] = None


    def _get_gs_index(self):
        self._data_nodes_index = pd.read_csv(
            os.environ["PATH_2_GS_INDEX"],
            index_col=None
        )

    def _append_2_table(
            self, 
            row_2_append: list[str, str]
    ):
        row = pd.DataFrame(
            data=[row_2_append],
            columns=["DataNodeIP","Path2File"]
        )
        self._data_nodes_index = pd.concat(
            [self._data_nodes_index, row],
            axis = 0
        )

    def _update_gs_index(self):
        self._data_nodes_index.to_csv(
            os.environ["PATH_2_GS_INDEX"],
            index = False
        )

    def update_table(
            self,
            row_2_append: list[str, str]
    ):
        self._get_gs_index()
        self._append_2_table(row_2_append)
        self._update_gs_index()


    def search_file(self, file_name:str) -> list[list[str,str]]:
        regex_pattern = fr"{file_name}"
        nodes_with_file:DataFrame = self._data_nodes_index[
            self._data_nodes_index["Path2File"].str.contains(
                regex_pattern,
                flags=re.IGNORECASE
            )
        ]
        return nodes_with_file.values.tolist()

    
    def get_data_nodes(self) -> DataFrame:
        return self._data_nodes_index
