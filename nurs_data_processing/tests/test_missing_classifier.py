import pytest
from ..missing_classifier import MissingClassifier
from ..missing_results import MissingResults
from .fixtures import missing_data
from sklearn import base


@pytest.fixture
def missing_classifier(missing_data):
    return MissingClassifier(missing_data)


def test_divide_by_data_type(missing_data):
    categorical, numeric = MissingClassifier.divide_by_data_type(missing_data, "object")
    assert categorical.shape[1] == 2
    assert numeric.shape[1] == 1


def test_prepare_data(missing_classifier):
    data_x, data_y = missing_classifier.prepare_data("Missing")
    assert data_x.shape[1] == 2
    assert data_x.shape[0] == data_y.shape[0]


def test_column(missing_classifier):
    result = missing_classifier.test_column("Missing")
    assert result.Variable == "Missing"
    assert isinstance(result.Model, base.BaseEstimator)
    assert len(result.Features) == 2
    assert isinstance(result.Score, float)


def test_all_columns(missing_classifier):
    results = missing_classifier.test_all_columns()
    assert isinstance(results, MissingResults)
    assert len(results) == 1
