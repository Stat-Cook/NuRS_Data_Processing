"""
Tools for mining the patterns of missingness in a data set.
"""
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.impute import SimpleImputer

from .encoded_label_data import EncodedLabelData
from .model_result import ClassifierResult
from .missing_results import MissingResults


class MissingClassifier:
    """

    Parameters
    ----------
    data: pd.DataFrame
        Data set for analysis of missing patterns
    numeric_imputer
        Method by which to impute numeric missing values
    """

    # pylint: ignore=too-many-instance-attributes

    def __init__(self, data: pd.DataFrame, numeric_imputer=SimpleImputer()):

        self.categorical_data, self.numeric_data = \
            self.divide_by_data_type(data, "object")

        self.categorical_columns = set(self.categorical_data.columns)
        self.numeric_columns = set(self.numeric_data.columns)

        self.encoded_categorical_data = EncodedLabelData(self.categorical_data)

        self.missing = data.isna()
        missing_sum = self.missing.sum() > 0
        self.missing_columns = missing_sum[missing_sum].index

        self.numeric_imputer = numeric_imputer

    @staticmethod
    def divide_by_data_type(data: pd.DataFrame, data_type: str):
        """
        Divide data into two data sets depending on data_type.
        Return a 2-tuple, where the first is a frame of the coumns of data_type and
        the second is a frame of the remainder.
        Parameters
        ----------
        data: pd.DataFrame
            data set to be divided
        data_type: str
            Data type to search for.
        Returns
        -------
        (pandas.DataFrame, pandas.DataFrame)
        """
        dtypes = data.dtypes
        is_data_type = dtypes[dtypes == data_type].index
        is_not_data_type = dtypes[dtypes != data_type].index
        return data[is_data_type], data[is_not_data_type]

    def prepare_numeric_data(self, missing_column):
        """
        Prepare numeric independent variables for mining.
        Parameters
        ----------
        missing_column: str
            The column being mined for.
        Returns
        -------
        pandas.DataFrame
        """
        numeric_columns = self.numeric_columns.difference([missing_column])
        if numeric_columns:
            numeric_x = self.numeric_data[numeric_columns]

            imputed_values = self.numeric_imputer.fit_transform(numeric_x)

            return pd.DataFrame(
                imputed_values,
                columns=numeric_x.columns
            )

        return pd.DataFrame()

    def prepare_categorical_data(self, missing_column):
        """
        Prepare categorical independent variables for mining.
        Parameters
        ----------
        missing_column: str
            The column being mined for.
        Returns
        -------
        pandas.DataFrame
        """
        categorical_columns = self.categorical_columns.difference([missing_column])
        if categorical_columns:

            categorical_x = [self.encoded_categorical_data[i] for i in categorical_columns]
            return pd.concat(categorical_x, axis=1)

        return pd.DataFrame()

    def prepare_data(self, missing_column):
        """
        Prepare dependent and independent variables for mining.
        Returns a 2-tuple of (independent, dependent).
        Parameters
        ----------
        missing_column: str
            The column being mined for.
        Returns
        -------
        (pandas.DataFrame, pandas.Series)
        """
        numeric_x = self.prepare_numeric_data(missing_column)
        categorical_x = self.prepare_categorical_data(missing_column)

        data_x = pd.concat([numeric_x, categorical_x], axis=1)
        data_y = self.missing[missing_column]

        return data_x, data_y

    def test_column(self, missing_column: str) -> ClassifierResult:
        """
        Test a single column for patterns of missingness.
        Parameters
        ----------
        missing_column: str
            Column to mine for patterns of missingness.
        Returns
        -------
        ClassifierResult
        """
        data_x, data_y = self.prepare_data(missing_column)
        train_x, test_x, train_y, test_y = train_test_split(data_x, data_y)
        model = DecisionTreeClassifier()
        model.fit(train_x, train_y)
        model_f1 = f1_score(test_y, model.predict(test_x))
        return ClassifierResult(missing_column, model, data_x.columns, model_f1)

    def test_all_columns(self):
        """
        Mine all columns with some data missing for patterns of missingness
        Returns
        -------
        MissingResults
        """
        missing_result = MissingResults()
        for col in self.missing_columns:
            missing_result.append(self.test_column(col))
        return missing_result


if __name__ == '__main__':

    N = 1000
    frm = pd.DataFrame({
        "A": np.random.normal(size=N),
        "B": np.random.choice(list("ABC"), N),
        "C": np.random.normal(size=N),
        "D": np.random.choice(list("ABCDEF"), N),
    })

    z = zip(
        np.random.choice(range(N), 50),
        np.random.choice(range(2), 50)
    )
    for i, j in z:
        frm.iloc[i, j] = None

    sel = (frm["D"] == "F")# & (np.random.uniform(0, 1, N) > 0.2)
    frm.loc[sel, "C"] = None
    frm.to_csv("nurs_data_processing/cli/tests/test_data/missing_data.csv")
    #
    # m1 = MissingClassifier(data)
    # print(m1.test_all_columns().to_markdown())
    # for col in m1.missing_columns:
    #     tree, labels, score = m1.test_column(col)
    #     z = zip(tree.feature_importances_, labels)
    #     print(f"Column:{col}")
    #     print(f"F1 score:{score}")
    #     for i,j in z:
    #         print(f"{j}:{i:.2f}")
