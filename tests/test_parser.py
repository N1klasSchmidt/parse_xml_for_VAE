import pytest
import sys
sys.path.append("/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/module")
from module.parser import xml_parser
from module.parser import dict_to_df
import os

def test_function_1():
    path_to_test_xml = "./testing_file.xml"
    result = None
    result = xml_parser(path_to_test_xml)
    assert result is not None
    assert isinstance(result, dict) 

def test_function_2():
    path_to_test_xml = "./testing_file.xml"
    result = xml_parser(path_to_test_xml)
    _ = dict_to_df(result, patient=1)
    for k, v in result.items():
        path = f"Aggregated_{k}.csv"
        assert os.path.exists(path)
