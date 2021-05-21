from ..missing_chart import metrics, group_vector
from .fixtures import missing_data


def test_categorical_metrics(missing_data):
    result = metrics(missing_data, "Missing", "Categorical")
    assert all(i in result for i in ["Feature", "Missing", "Lower", "Upper"])
    assert result["Feature"] == "A"


def test_numeric_metrics(missing_data):
    result = metrics(missing_data, "Missing", "Numeric")
    assert all(i in result for i in ["Feature", "Missing", "Lower", "Upper"])
    assert isinstance(result["Feature"], float)


def test_group_vector_categorical(missing_data):
    vector = group_vector(missing_data, "Categorical")
    unique = vector.unique()
    assert len(unique) == 2


def test_group_vector_categorical_missing(missing_data):
    vector = group_vector(missing_data, "Missing")
    unique = vector.unique()
    assert len(unique) == 4


def test_group_vector_numeric(missing_data):
    vector = group_vector(missing_data, "Numeric")
    unique = vector.unique()
    assert len(unique) == 10
