import pytest
import sys
sys.path.append("/net/data.isilon/ag-cherrmann/nschmidt/project/parse_xml_for_VAE/module")
from module.parser import function

def test_function_1():
    result = function(1)
    assert result == 1

def test_function_2():
    result = function(2)
    assert result == 4

def test_function_3():
    result = function(3)
    assert result == 6 

