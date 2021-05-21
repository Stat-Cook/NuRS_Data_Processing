import pytest

@pytest.fixture
def test_data_folder():
    return "nurs_data_processing/tests/test_data/"


@pytest.fixture
def test_data_path(test_data_folder):
    return f"{test_data_folder}missing_data.csv"
