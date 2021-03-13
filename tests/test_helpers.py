import pytest
from fx_api.helpers import is_string_or_list_of_strings

def test_is_string_or_list_of_strings_str():
    """Test str object returns True
    """
    assert is_string_or_list_of_strings("test string") == True

def test_is_string_or_list_of_strings_list():
    """Test list of str object returns True
    """
    assert is_string_or_list_of_strings(["str1", "str2"]) == True

def test_is_string_or_list_of_strings_fail_int():
    """Test int object returns False
    """
    assert is_string_or_list_of_strings(123) == False

def test_is_string_or_list_of_strings_fail_list():
    """Test list of non-str object returns False
    """
    assert is_string_or_list_of_strings(["str1", False]) == False


