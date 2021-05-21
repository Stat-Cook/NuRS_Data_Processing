import pytest
from .utilities import missing_mining_checks
from ..missing_results import MissingResults

def test_type_is_MissingResults():
    values = [1,2,3]
    with pytest.raises(TypeError):
        missing_mining_checks(values, n=3)


def test_length():
    values = MissingResults([1,2,3])
    with pytest.raises(AttributeError):
        missing_mining_checks(values, n=4)


def test_type_is_ClassifierModel():
    values = MissingResults([1,2,3])
    with pytest.raises(TypeError):
       missing_mining_checks(values, n=3)