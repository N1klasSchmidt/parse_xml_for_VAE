import pathlib

from utils.config_utils import Config
from module.parser_v2 import valid_patients, process_all_paths
from module.data_processing import load_mri_data_2D, load_mri_data_2D_all_atlases


config = Config(
    RAW_DATA_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/testing_files",  #"/net/data.isilon/ag-cherrmann/stumrani/mri_prep", 
    EXTRACTED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/xml_data",
    EXTRACTED_CSV_T_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/xml_data_t",
    PROCESSED_CSV_DIR = "/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/processed_data",
    METADATA_PATHS = ["./metadata_20250110/full_data_train_valid_test.csv",
                      "./metadata_20250110/meta_data_NSS_all_variables.csv",
                      "./metadata_20250110/meta_data_whiteCAT_all_variables.csv"], 
    ALL_ATLASES = False
)


def get_all_data(directory: str, ext: str = "h5") -> list:
    data_paths = list(pathlib.Path(directory).rglob(f"*.{ext}"))
    return data_paths


valid_patients = valid_patients(config.METADATA_PATHS)
process_all_paths(directory=config.RAW_DATA_DIR,
                  valid_patients=valid_patients,
                  batch_size=5)

# Convert data from per atlas to per patient, either with all atlases or only using one. 
if config.ALL_ATLASES is False: 
    subjects_all, data_overview = load_mri_data_2D(data_path="./xml_data/Aggregated_suit.h5",  # Here a concrete example, but this can be anything.
                                                   csv_paths=config.METADATA_PATHS,
                                                   hdf5=True)

elif config.ALL_ATLASES is True: 
    data_paths = get_all_data(directory=config.EXTRACTED_CSV_DIR, ext="h5")
    subjects_all, data_overview = load_mri_data_2D_all_atlases(data_paths=data_paths,
                                                               csv_paths=config.METADATA_PATHS,
                                                               hdf5=True)
    print(subjects_all)
else: 
    print("Please specify if all atlases should be processed, or only one.")
                                                    