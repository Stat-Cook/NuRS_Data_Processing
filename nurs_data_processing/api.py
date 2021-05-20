"""
API bindings to the missing mining functions
"""
import pandas as pd
from .missing_classifier import MissingClassifier
from .missing_results import MissingResults


def mine_missing_features(file_path: str, sheet_name=0) -> MissingResults:
    """
    Mine a data set loaded from file for patterns of missingness.
    Parameters
    ----------
    file_path: str
        path to data set
    sheet_name: Union[int, str] [optional]
        Sheet ID of the data set to mine

    Returns
    -------
    MissingResults
    """
    if file_path.lower().endswith(".csv"):
        data = pd.read_csv(file_path)
    if file_path.lower().endswith((".xls", ".xlsx")):
        data = pd.read_excel(file_path, sheet_name=sheet_name)

    missing_classifier = MissingClassifier(data)
    return missing_classifier.test_all_columns()


def mine_missing(data: pd.DataFrame) -> MissingResults:
    """
    Mine a data set for patterns of missingness
    Parameters
    ----------
    data: pandas.DataFrame
        The data set to be investigated

    Returns
    -------
    MissingResults
    """
    missing_classifier = MissingClassifier(data)
    return missing_classifier.test_all_columns()
