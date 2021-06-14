from nurs_data_processing.cli import mine_missing_features as mmf
from .. import test_data_path, test_data_folder


def test_main(test_data_path):
    mmf.main([test_data_path])


def test_main_to_file(test_data_path):
    mmf.main([test_data_path, "-m", "markdown", "-e", "temp.md"])
