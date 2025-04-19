import pathlib

from utils.config_utils import Config
from module.parser_v2 import valid_patients, process_all_paths
from module.data_processing import load_mri_data_2D, load_mri_data_2D_all_atlases


config_train = Config(
    RAW_DATA_DIR = "/net/data.isilon/ag-cherrmann/stumrani/mri_prep", #"/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/testing_files", 
    EXTRACTED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/train_xml_data",
    EXTRACTED_CSV_T_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/train_xml_data_t",
    PROCESSED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/train_processed_data",
    METADATA_PATHS = ["./metadata_20250110/full_data_train_valid_test.csv",
                      "./metadata_20250110/meta_data_NSS_all_variables.csv",
                      "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"], 
    ALL_ATLASES = True,
    TRAIN_DATA = True,
    TEST_DATA = ["whitecatnii", "whiteCAT_updt","nss_updt", "NSSnii"]
)


def get_all_data(directory: str, ext: str = "h5") -> list:
    data_paths = list(pathlib.Path(directory).rglob(f"*.{ext}"))
    return data_paths


valid_patients = valid_patients(config_train.METADATA_PATHS)

process_all_paths(directory=config_train.RAW_DATA_DIR,
                  valid_patients=valid_patients,
                  batch_size=10,
                  train=config_train.TRAIN_DATA,
                  test_data=config_train.TEST_DATA,
                  hdf5=True)

# Convert data from per atlas to per patient, either with all atlases or only using one. 
# if config_train.ALL_ATLASES is False: 
#     subjects_all, data_overview = load_mri_data_2D(data_path="./xml_data/Aggregated_suit.h5",  # Here a concrete example, but this can be anything.
#                                                    csv_paths=config_train.METADATA_PATHS,
#                                                    hdf5=True)

# elif config_train.ALL_ATLASES is True: 
#     data_paths = get_all_data(directory=config_train.EXTRACTED_CSV_DIR, ext="h5")
#     subjects_all, data_overview = load_mri_data_2D_all_atlases(data_paths=data_paths,
#                                                                csv_paths=config_train.METADATA_PATHS,
#                                                                hdf5=True)
    
# else: 
#     print("Please specify if all atlases should be processed, or only one.")
                                                    