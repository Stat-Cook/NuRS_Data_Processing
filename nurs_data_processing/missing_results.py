"""
Tools for managing multiple missing mining results at the same time.
"""
from collections import UserList
import pandas as pd
from nurs_data_processing.model_result import ClassifierResult


class MissingResults(UserList):

    """
    List of ClassifierResult objects.
    Parameters
    ----------
    values [optional]
        Initial values of the list
    """

    # pylint: ignore=too-many-ancestors
    def __init__(self, value=None):
        super().__init__(value)

    def append(self, item: ClassifierResult) -> None:
        """
        Add extra item to self
        Parameters
        ----------
        item: ClassifierResult
            the result to be added
        """
        if isinstance(item, ClassifierResult):
            super().append(item)
        else:
            raise TypeError(f"Expected item of type 'ClassifierResult', but received {type(item)}")

    def __iadd__(self, other):
        """
        Add extra item to self
        Parameters
        ----------
        other: ClassifierResult
            the result to be added

        """
        if all(isinstance(item, ClassifierResult) for item in other):
            super().__add__(other)
        else:
            raise TypeError("Expected all item to be of type 'ClassifierResult'")

    def __str__(self):
        string = ""
        for i in self:
            zipped = zip(i.Features, i.Model.feature_importances_)
            zipped = "\n".join([f"{i}:{j:.3f}" for i, j in zipped])

            loop_string = f"Column: {i.Variable} \n" \
                          f"F1-score: {i.Score:.3f} \n" \
                          f"{zipped}\n"
            string += loop_string

        return string

    def to_markdown(self, n_features=5):
        """
        Produce a report on every ClassifierResult in self.
        Returns the K top performing features.
        Parameters
        ----------
        n_features: int [optional]
            Number of top features to return in report.

        Returns
        -------
        str
        """
        string = ""
        for i in self:
            frm = pd.DataFrame(
                zip(i.Features, i.Model.feature_importances_),
                columns=["Feature", "Feature Importance"]
            )
            frm = frm.sort_values("Feature Importance", ascending=False)[:n_features]
            frm["Feature"] = frm["Feature"].apply(self.format_feature_string)

            loop_string = f"## Column: {i.Variable} \n" \
                          f"### F1-score: {i.Score:.3f} \n" \
                          f"{frm.to_markdown(index=False)}\n"
            string += loop_string
        return string

    @staticmethod
    def format_feature_string(feature):
        """
        Convert feature to human readable format.
        Parameters
        ----------
        feature: Union(str, tuple)
            Label of the feature.
        Returns
        -------
        str
        """
        if isinstance(feature, tuple):
            return f"Variable:{feature[0]}, Value:{feature[1]}"

        return f"Variable:{feature}"
