import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def missing_data():
    np.random.seed(1001)
    frame = pd.DataFrame({
        "Numeric": np.random.normal(size=100),
        "Categorical": 60*["A"] + 40*["B"],
        "Missing": np.random.choice(list("ABC"), 100)
    })
    frame.loc[1:10, "Missing"] = None
    return frame
