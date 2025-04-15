import pathlib

from utils.config_utils import Config
from module.parser import valid_patients, process_all_paths
from module.data_processing import load_mri_data_2D, load_mri_data_2D_all_atlases


config = Config(
    RAW_DATA_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/testing_files",
    EXTRACTED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/xml_data",
    EXTRACTED_CSV_T_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/xml_data_t",
    PROCESSED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/processed_data",
    METADATA_PATHS = ["./metadata_20250110/full_data_train_valid_test.csv",
                      "./metadata_20250110/meta_data_NSS_all_variables.csv",
                      "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"], 
    ALL_ATLASES = True
)


def get_all_data(directory: str) -> list:
    data_paths = list(pathlib.Path(directory).rglob("*.csv"))
    return data_paths


valid_patients = valid_patients(config.METADATA_PATHS)
process_all_paths(directory=config.RAW_DATA_DIR,
                  valid_patients=valid_patients)


if config.ALL_ATLASES is False: 
    load_mri_data_2D(data_path="./xml_data/Aggregated_suit.csv",  # Here a concrete example, but can be anything.
                     csv_path=config.METADATA_PATHS[0])  # The code here should be changed to accept all the metadata files. Or merge all the metadata files to a single df. 
                    
elif config.ALL_ATLASES is True: 
    subjects_all, data_overview = load_mri_data_2D_all_atlases(data_paths=get_all_data(config.EXTRACTED_CSV_DIR),
                                                               csv_path=config.METADATA_PATHS[0])

else: 
    print("Please specify if all atlases should be processed, or only one.")
                                                    