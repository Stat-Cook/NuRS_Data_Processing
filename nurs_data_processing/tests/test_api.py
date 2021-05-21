from . import test_data_path, test_data_folder
from ..api import mine_missing, mine_missing_from_file
from .utilities import missing_mining_checks

def test_mine_from_file(test_data_path):
    result = mine_missing_from_file(test_data_path)
    missing_mining_checks(result, n=3)
