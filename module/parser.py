import numpy as np 
import pytest
import xml.etree.ElementTree as ET
import pandas as pd
import os
import pathlib
import regex as re

def xml_parser(path_to_xml_file: str) -> dict:

    tree = ET.parse(path_to_xml_file)
    root = tree.getroot()
    results = {}

    for section in root: 
        section_name = section.tag
        results[section_name] = {}

        names_element = section.find("names")
        if names_element is not None: 
            names = []
            for item in names_element.findall("item"):
                names.append(item.text)
            results[section_name]["names"] = names
        
        data_element = section.find("data")
        if data_element is not None:
            for data_type in data_element: 
                data_tag = data_type.tag
                data = [float(val) for val in data_type.text.strip("[]").split(";")]
                results[section_name][data_tag] = data

    return results


def dict_to_df(data_dict: dict, patient: str):

    for k, v in data_dict.items():
        filepath = f"./Aggregated_{k}.csv"  # Added file extension
        
        volumes = [vs for vs in v.keys() if vs != "names"]

        arrays = [[patient]*len(volumes), volumes]

        tuples = list(zip(*arrays))

        index = pd.MultiIndex.from_tuples(tuples, names = ["Patient", "Volume"])

        if "names" not in v:
            print(f"No names found in section {k}, skipping.")
       
        data = {volume: v[volume] for volume in volumes}
        df_new = pd.DataFrame(data, index=v["names"])
        df_new.columns = index
        # Check if file exists and has content
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            # If file doesn't exist or is empty, just save the new dataframe
            df_new.to_csv(filepath)
        else:
            try:
                # Read existing file with proper MultiIndex handling
                df_existing = pd.read_csv(filepath, header=[0, 1], index_col=0)
                
                # Concatenate horizontally while preserving MultiIndex
                result = pd.concat([df_existing, df_new], axis=1)
                
                # Save with MultiIndex preserved
                result.to_csv(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                # Fallback - just write the new data
                df_new.to_csv(filepath)
    return
    

def get_all_xml_paths(directory: str, valid_patients: list) -> list:
    xml_paths = pathlib.Path(directory).rglob("*.xml")
    xml_paths = list(xml_paths)
    xml_paths = [str(i) for i in xml_paths]

    partial_set = set(valid_patients)
    filtered_paths = [
        xml_path for xml_path in xml_paths
        if any(partial_path in xml_path for partial_path in partial_set)
    ]
    
    return filtered_paths


def process_all_paths(directory: str, valid_patients: list): 
    paths = get_all_xml_paths(directory, valid_patients)
    print(f"Found a total of {len(paths)} valid patient .xml files.")
    # First, identify all section types that will be processed
    section_types = set()
    for path in paths:
        parsed_dict = xml_parser(path)
        section_types.update(parsed_dict.keys())
    
    # Clear existing files at the beginning
    for section in section_types:
        filepath = f"./Aggregated_{section}.csv"
        if os.path.exists(filepath):
            # Clear the file by opening in write mode
            with open(filepath, "w+") as f:
                f.close()
    
    # Now process each XML file
    for idx, path in enumerate(paths): 
        print(f"Processing file {idx+1}/{len(paths)}: {path}")
        parsed_dict = xml_parser(path)

        match_no_ext = re.search(r"([^/\\]+)$", path)
        if match_no_ext:
            patient_id = match_no_ext.group(1)
        dict_to_df(parsed_dict, patient=patient_id)
    return


def transpose_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    return


def valid_patients(paths: list) -> list:
    valid_list = []

    for path in paths: 
        df = pd.read_csv(path) 
        list_of_patients = df['Filename'].tolist()
        valid_list += list_of_patients
    return valid_list


if __name__ == "__main__":
    directory = "./testing_files"

    paths_to_consider = ["./metadata_20250110/full_data_train_valid_test.csv",
                        "./metadata_20250110/meta_data_NSS_all_variables.csv",
                        "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"]

    valid_patients = valid_patients(paths_to_consider)
    
    process_all_paths(directory=directory, valid_patients=valid_patients)
