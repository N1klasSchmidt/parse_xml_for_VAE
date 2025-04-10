import pytest
import sys
sys.path.append("/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/module")
from module.parser import xml_parser, valid_patients, dict_to_df, get_all_xml_paths
import os
import pathlib
import pandas as pd

def test_parser():
    path_to_test_xml = "./testing_files/dataset_1/label/catROI_IXI541-IOP-1146-T1.xml"
    result = None
    result = xml_parser(path_to_test_xml)
    assert result is not None
    assert isinstance(result, dict) 

# def test_dict_to_df():
#     path_to_test_xml = "./testing_files/dataset_1/label/testing_file_IXI541-IOP-1146-T1.xml"
    
#     result = xml_parser(path_to_test_xml)
#     _ = dict_to_df(result, patient=1)
#     for k, v in result.items():
#         path = f"Aggregated_{k}.csv"
#         assert os.path.exists(path)
#         assert os.path.getsize(path) != 0

def test_multiple_file_processing():
    test_dir = "testing_files/"
    paths_to_consider = ["./metadata_20250110/full_data_train_valid_test.csv",
                        "./metadata_20250110/meta_data_NSS_all_variables.csv",
                        "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"]
    
    pat_list = valid_patients(paths_to_consider)
    path_list = get_all_xml_paths(test_dir, valid_patients=pat_list)
    assert isinstance(path_list, list)
    assert len(path_list) == 2


def test_valid_patients():
    paths_to_consider = ["./metadata_20250110/full_data_train_valid_test.csv",
                        "./metadata_20250110/meta_data_NSS_all_variables.csv",
                        "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"]
    
    pat_list = valid_patients(paths_to_consider)
    assert len(pat_list) != 0
    
