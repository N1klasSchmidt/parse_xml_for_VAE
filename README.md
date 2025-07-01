# Parser for XML Neuroimaging Data

These scripts can be used to extract and parse from a directory all the .xml files into a more readable and aggregated .csv or .h5 format. These files must have the same general structure.

Python 3.13.2 was used to run and test the code. Further requirements can be found in the requirements.txt file. 

## Folder Structure
Parser_XML_for_VAE
|── `module`:                             for storing all the parsing scripts  
|── `tests`:                              for storing all the tests
|── `utils`:                              for config utils
|── `metadata`:                           for storing all the relevant metadata
|── `run_preprocessing_test.py`:          to run the preprocessing and extract training data
|── `run_preprocessing_train.py`:         to run the preprocessing and extract testing data

## Functionality
The current parser, found in module/parser_v2.py is specifically configured to extract brain segmentation volumes extracted from MRI scans through the CAT12 software (https://neuro-jena.github.io/cat12-help/).

The workflow is as follows: 
- Determine directory from which .xml files should be parsed.
- Specify if there are any subfolders to consider.
- Use run_preprocessing_train.py and run_preprocessing_test.py by specifying which folders within the target directory should be used for testing. 
- Data for each atlas is saved separately, aggregating all patients in a single data frame. 
- Copy data as needed to other projects.

The code was specifically used to prepare the input data for the VAE models in https://github.com/N1klasSchmidt/catatonia_VAE_2D. Besides the core parsing functionality there is also some very rudimentary data analysis code in the Jupyter Notebooks.