import os
# import torch  # How to check nvidia-smi version???
import pandas as pd
import regex as re
from typing import List, Tuple
import numpy as np


def flatten_array(df: pd.DataFrame) -> np.ndarray:
    array = df.to_numpy()
    flat_array = array.flatten()
    return flat_array


class CustomDataset(Dataset):  # Create Datasets that can then be converted into DataLoader objects
    def __init__(self, subjects, transforms=None):
        self.subjects = subjects
        self.transforms = transforms

    def __len__(self):
        return len(self.subjects)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        measurements = self.subjects[idx]["measurements"]
        labels = self.subjects[idx]["labels"]

        if self.transform:
            transformed = self.transforms(measurements=measurements)
            measurements = transformed['measurements']

        measurements = torch.as_tensor(measurements, dtype=torch.float64)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        return measurements, labels


def load_mri_data_2D(
    # The path to the directory where the MRI data is stored (.csv file formats)
    data_path: str,
    # The path to the CSV file that contains the filenames of the MRI data and the diagnoses and covariates
    csv_path: str = None,
    # The annotations DataFrame that contains the filenames of the MRI data and the diagnoses and covariates
    annotations: pd.DataFrame = None,
    # The diagnoses that you want to include in the data loading, defaults to all
    diagnoses: List[str] = None,
    covars: List[str] = [],
) -> Tuple:

    # If the CSV path is provided, check if the file exists, make sure that the annotations are not provided
    if csv_path is not None:
        assert os.path.isfile(csv_path), f"CSV file '{csv_path}' not found"
        assert annotations is None, "Both CSV and annotations provided"

        # Initialize the data overview DataFrame
        data_overview = pd.read_csv(csv_path)

    # If the annotations are provided, make sure that they are a pandas DataFrame, and that the CSV path is not provided
    if annotations is not None:
        assert isinstance(
            annotations, pd.DataFrame
        ), "Annotations must be a pandas DataFrame"
        assert csv_path is None, "Both CSV and annotations provided"

        # Initialize the data overview DataFrame
        data_overview = annotations

    # If no diagnoses are provided, use all diagnoses in the data overview
    if diagnoses is None:
        diagnoses = data_overview["Diagnosis"].unique().tolist()

    # If the covariates are not a list, make them a list
    if not isinstance(covars, list):
        covars = [covars]

    # If the diagnoses are not a list, make them a list
    if not isinstance(diagnoses, list):
        diagnoses = [diagnoses]
    
    # Set all the variables that will be one-hot encoded
    variables = ["Diagnosis"] + covars

    # Filter unwanted diagnoses
    data_overview = data_overview[data_overview["Diagnosis"].isin(diagnoses)]

    # produce one hot coded labels for each variable
    one_hot_labels = {}
    for var in variables:
        # check that the variables is in the data overview
        if var not in data_overview.columns:
            raise ValueError(f"Column '{var}' not found in CSV file or annotations")

        # one hot encode the variable
        one_hot_labels[var] = pd.get_dummies(data_overview[var], dtype=float)

    # For each subject, collect MRI data and variable data in the Subject object
    subjects = []

    data = pd.read_csv(data_path)
    data.set_index("Filename", inplace=True)
    all_file_names = data.index

    for index, row in data_overview.iterrows():
        subject = {} 
        
        if not row["Filename"] in all_file_names:
            continue

        # Format correct filename
        if row["Filename"].endswith(".nii") or row["Filename"].endswith(".nii.gz"):
            pre_file_name = row["Filename"]
            match_no_ext = re.search(r"([^/\\]+)\.[^./\\]*$", pre_file_name)  # Extract file stem
            if match_no_ext:
                file_name = match_no_ext.group(1)
        else:
            file_name = row["Filename"]

        patient_data = data.loc[file_name]
        flat_patient_data = flatten_array(patient_data).tolist()
        
        subject["name"] = file_name
        subject["measurements"] = flat_patient_data
        subject["labels"] = {}

        # Add one hot encoded labels to subject
        #for var in variables:
        #    subject[var] = torch.tensor(
        #        one_hot_labels[var].loc[index].values, dtype=torch.float
        #    )

        for var in variables:
            subject["labels"][var] = one_hot_labels[var].loc[index].to_numpy().tolist()

        # Store Subject in our list
        subjects.append(subject)

    # Return the list of subjects and the filtered annotations
    return subjects, data_overview


# This function processes a list of subjects by applying a series of transformations to them, and then loads
# them into a DataLoader object.
def process_subjects(
    # The list of tio.Subject objects that you want to process
    subjects: List,
    # The transformations that you want to apply to the subjects
    transforms: torch.compose,
    # The batch size for the DataLoader (the larger, the more memory is needed)
    batch_size: int,
    # Whether the data should be shuffled or not. Shuffling is important for training, but not for validation.
    shuffle_data: bool,
) -> DataLoader:

    # Apply transformations
    dataset = CustomDataset(subjects=subjects, transforms=transform)

    # Create data loader
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle_data)

    # Return the DataLoader object
    return data_loader
