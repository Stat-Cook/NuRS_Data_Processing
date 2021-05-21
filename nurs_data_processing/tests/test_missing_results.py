import pytest
from ..missing_results import MissingResults
from ..model_result import ClassifierResult
from .test_missing_classifier import missing_classifier, missing_data

@pytest.fixture
def empty_result():
    return MissingResults([])


@pytest.fixture
def classifier_result(missing_classifier):
    return missing_classifier.test_column("Missing")


@pytest.fixture
def model_result(classifier_result):
    return MissingResults([classifier_result, classifier_result])


def test_append_fails(empty_result):
    with pytest.raises(TypeError):
        empty_result.append(12)


def test_iadd_fails(empty_result):
    with pytest.raises(TypeError):
        empty_result += [1]


def test_iadd_fails2(empty_result):
    with pytest.raises(TypeError):
        empty_result += [1, 2]


def test_append(empty_result):
    empty_result.append(ClassifierResult(1, 2, 3, 4))


def test_iadd(empty_result):
    empty_result += [ClassifierResult(1, 2, 3, 4)]


def test_to_markdown(model_result):
    markdown = model_result.to_markdown()
    assert isinstance(markdown, str)


def test_format_string_1(model_result):
    string = model_result.format_feature_string("A")
    assert string == "Variable:A"


def test_format_string_2(model_result):
    string = model_result.format_feature_string(("A", "1"))
    assert string == "Variable:A, Value:1"
