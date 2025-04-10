import pytest
import pandas as pd
from module.data_processing import load_mri_data_2D, flatten_array

def test_loading(): 
    path = "./xml_data/Aggregated_suit_t.csv"
    df = pd.read_csv(path)
    file_name = "4038_01_MR_T1w_MPR"
    df.set_index("Filename", inplace=True)
    patient_data = df.loc[file_name]
    patient_data_np = patient_data.to_numpy()
    assert patient_data.shape == (2, 29)

def test_flattening():
    path = "./xml_data/Aggregated_suit_t.csv"
    df = pd.read_csv(path)
    file_name = "4038_01_MR_T1w_MPR"
    df.set_index("Filename", inplace=True)
    patient_data = df.loc[file_name]
    patient_data = patient_data.copy()
    
    flat_data = flatten_array(patient_data)

    assert flat_data.shape == (58,)

def test_mri_2D():
    subjects, overview = load_mri_data_2D(data_path="./xml_data/Aggregated_suit_t.csv",
                                          csv_path="./metadata_20250110/full_data_train_valid_test.csv")
    assert isinstance(subjects, list)
    assert isinstance(overview, pd.DataFrame)
    assert len(subjects) == 2



