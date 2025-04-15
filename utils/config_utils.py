import os
import pathlib
from typing import List

def add_to_gitignore(path: str):
    with open(".gitignore", "a") as g:
        g.write(f"{path}")
        g.write("\n")
    return


'''
Config class to set up all parameters for model preparation and training. Is used with the run_ModelXYZ.py scripts.
'''

# Set up all parameters for model preparation and training
class Config:

    def __init__(
        self,
        # The learning rate for the model optimizer
        RAW_DATA_DIR = None,
        EXTRACTED_CSV_DIR = None,
        EXTRACTED_CSV_T_DIR = None,
        PROCESSED_CSV_DIR = None,
        METADATA_PATHS = None,  
        ALL_ATLASES = False,

    ):

        for path in [RAW_DATA_DIR, METADATA_PATHS]:
            if path is not None:
                if not isinstance(path, list):
                    assert os.path.exists(path), f"Path {path} does not exist"
                else: 
                    for p in path: 
                        assert os.path.exists(p), f"Path {p} does not exist"
        # set up paths
        self.RAW_DATA_DIR = RAW_DATA_DIR
        self.EXTRACTED_CSV_DIR = EXTRACTED_CSV_DIR
        self.EXTRACTED_CSV_T_DIR = EXTRACTED_CSV_T_DIR
        self.PROCESSED_CSV_DIR = PROCESSED_CSV_DIR
        self.METADATA_PATHS = METADATA_PATHS
        self.ALL_ATLASES = ALL_ATLASES

        metadata_parent = pathlib.Path(self.METADATA_PATHS[0]).parents[0]
        
        add_to_gitignore(str(metadata_parent))

        # set up run specific output directories
        for path in [
            self.EXTRACTED_CSV_DIR, 
            self.EXTRACTED_CSV_T_DIR, 
            self.PROCESSED_CSV_DIR,
        ]:
            # make sure it doesn't already exist
            assert not os.path.exists(
                path
            ), f"Path {path} already exists, and may be overwritten. Please rename or remove it."
            # create the directory
            os.makedirs(path)
        
        for path in [
            self.RAW_DATA_DIR,
            self.EXTRACTED_CSV_DIR, 
            self.EXTRACTED_CSV_T_DIR, 
            self.PROCESSED_CSV_DIR,
        ]:
            basename = os.path.basename(path)
            add_to_gitignore(basename)

    def __str__(self):
        return str(vars(self))