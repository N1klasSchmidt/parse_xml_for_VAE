import numpy as np 
import pytest
import xml.etree.ElementTree as ET
import pandas as pd
import os
import pathlib

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


def dict_to_df(data_dict: dict, patient: int):


    for k, v in data_dict.items():
        filepath = f"./Aggregated_{k}.csv"  # Added file extension
        
        volumes = []
        for vs in v.keys():
            if vs != "names":
                volumes.append(vs)

        arrays = [[patient]*len(volumes), volumes]

        tuples = list(zip(*arrays))

        index = pd.MultiIndex.from_tuples(tuples, names = ["Patient", "Volume"])

        # Create DataFrame from the new dictionary
        df_new = pd.DataFrame.from_dict(v)
        df_new = df_new.set_index("names")
        df_new.columns = index
        # Check if file exists and has content
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            # If file doesn't exist or is empty, just save the new dataframe
            df_new.to_csv(filepath)
        else:
            # If file exists and has content, read it, concat, and save
            try:
                df_existing = pd.read_csv(filepath, index_col=0)  # Assuming names is the index
                result = pd.concat([df_existing, df_new], axis=1)  # Concatenate horizontally
                result.to_csv(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                # Fallback - just write the new data
                df_new.to_csv(filepath)
        
    return
    

def get_all_xml_paths(directory: str) -> list:
    xml_paths = pathlib.Path(directory).rglob("*.xml")
    xml_paths = list(xml_paths)
    return xml_paths


def process_all_paths(directory: str): 
    paths = get_all_xml_paths(directory)

    for idx, path in enumerate(paths): 
        print(idx, path)
        parsed_dict = xml_parser(path)
        
        if idx == 0: 
            for k, v in parsed_dict.items():
                filepath = f"./Aggregated_{k}.csv"
                if os.path.exists(filepath):
                    if os.path.getsize(filepath) != 0:
                        f = open(filepath, "w+")
                        f.close()

        dict_to_df(parsed_dict, patient=idx)
    return


if __name__ == "__main__":
    directory = "./testing_files"
    process_all_paths(directory=directory)
