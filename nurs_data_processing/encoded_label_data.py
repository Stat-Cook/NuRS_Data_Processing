"""
Tools for caching results of One Hot Vector encoding on categorical data.
"""
import pandas as pd
from sklearn.preprocessing import LabelBinarizer


class EncodedLabelData:
    """
    One hot vector encodings  of the supplied data set.
    [see https://en.wikipedia.org/wiki/One-hot if unsure what a one-hot
    representation is]

    Parameters
    ----------
    data: pd.DataFrame
        A data set where each column is made up of categorical variables
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.frames = {}
        self._initialize_values()
        self.columns = self.data.columns

    @staticmethod
    def label_binarize_column(column: pd.Series):
        """
        Convert a single column of data to a one hot vector encoding.
        Parameters
        ----------
        column: pd.Series
            A column of data, consisting of categorical values.
        Returns
        -------
        pd.DataFrame
        """
        name = column.name
        enc = LabelBinarizer()
        binarized = enc.fit_transform(column.fillna("NaN"))
        if len(enc.classes_) == 2:
            classes = [enc.classes_[1]]
        else:
            classes = enc.classes_
        return pd.DataFrame(
            binarized,
            columns=[(name, i) for i in classes]
        )

    def _initialize_values(self):
        """
        Iterates through all self.data columns creating the one-hot-vector
        representation.
        Returns
        -------
        None
        """
        for col in self.data.columns:
            self.frames[col] = self.label_binarize_column(self.data[col])

    def __getitem__(self, item):
        return self.frames[item]
