import pytest
import sys
sys.path.append("/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/module")
from module.parser import xml_parser
from module.parser import dict_to_df
from module.parser import get_all_xml_paths
import os
import pathlib

def test_parser():
    path_to_test_xml = "./testing_files/dataset_1/label/testing_file.xml"
    result = None
    result = xml_parser(path_to_test_xml)
    assert result is not None
    assert isinstance(result, dict) 

def test_dict_to_df():
    path_to_test_xml = "./testing_files/dataset_1/label/testing_file.xml"
    result = xml_parser(path_to_test_xml)
    _ = dict_to_df(result, patient=1)
    for k, v in result.items():
        path = f"Aggregated_{k}.csv"
        assert os.path.exists(path)
        assert os.path.getsize(path) != 0

def test_multiple_file_processing():
    test_dir = "./testing_files/"
    path_list = get_all_xml_paths(test_dir)
    assert isinstance(path_list, list)
    assert len(path_list) == 2
