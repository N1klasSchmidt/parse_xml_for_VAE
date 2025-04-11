import pytest
import pandas as pd
import pathlib
from module.data_processing import load_mri_data_2D, flatten_array, normalize_df, load_mri_data_2D_all_atlases, get_all_data, get_atlas

def test_loading(): 
    path = "./xml_data/Aggregated_suit.csv"
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    file_name = "4038_01_MR_T1w_MPR"
    patient_data = df[file_name]
    patient_data_np = patient_data.to_numpy()
    assert patient_data.shape == (28, 2)

def test_flattening():
    path = "./xml_data/Aggregated_suit.csv"
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    file_name = "4038_01_MR_T1w_MPR"
    patient_data = df[file_name]
    patient_data = patient_data.copy()
    
    flat_data = flatten_array(patient_data)

    assert flat_data.shape == (56,)

def test_mri_2D():
    subjects, overview = load_mri_data_2D(data_path="./xml_data/Aggregated_suit.csv",
                                          csv_path="./metadata_20250110/full_data_train_valid_test.csv")
    assert isinstance(subjects, list)
    assert isinstance(overview, pd.DataFrame)
    assert len(subjects) == 2


def test_normalization():
    path = "./xml_data/Aggregated_suit.csv"
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    df_norm = normalize_df(df)
    assert df.shape == df_norm.shape

def test_auto_process():
    data_paths = get_all_data("./xml_data")
    subjects, data_overview = load_mri_data_2D_all_atlases(data_paths=data_paths,
                                                           csv_path="./metadata_20250110/full_data_train_valid_test.csv")
    assert isinstance(subjects, list) and isinstance(data_overview, pd.DataFrame)
    assert len(subjects) == 2
    
def test_get_atlas():
    path = pathlib.Path(r"./xml_data/Aggregated_thalamic_nuclei.csv")
    atlas = get_atlas(path)
    assert atlas == "thalamic_nuclei"

