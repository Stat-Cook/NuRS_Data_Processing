import pytest
import numpy as np
import pandas as pd
from ..encoded_label_data import EncodedLabelData


@pytest.fixture
def eld_fixture():
    return EncodedLabelData(pd.DataFrame({
        "A": np.random.choice(list('ABC'), 40),
        "B": np.random.choice(list("ABC"), 40)
    }))


def test_indexing(eld_fixture: EncodedLabelData):
    cases, features = eld_fixture["A"].shape
    assert cases == 40
    assert features == 3


def test_binarizer(eld_fixture: EncodedLabelData):
    value = pd.Series(list("ABC"))
    binarized = eld_fixture.label_binarize_column(value)
    assert all(map(all, binarized.values == np.identity(3)))


def test_binarizer_nans(eld_fixture: EncodedLabelData):
    value = pd.Series(["A", "B", "C", None], name="Test")
    binarized = eld_fixture.label_binarize_column(value)
    assert ("Test", "NaN") in binarized.columns
    assert all(map(all, binarized.values == np.identity(4)))
