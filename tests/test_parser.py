import pytest
from src import parser

def test_function_1():
    result = parser.function(2)
    assert result == 4

def test_function_2():
    result = parser.function(3)
    assert result == 6

print("Hello World")