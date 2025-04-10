import pathlib

def get_all_data(directory: str) -> list:
    data_paths = list(pathlib.Path(directory).rglob("*.csv"))
    return data_paths