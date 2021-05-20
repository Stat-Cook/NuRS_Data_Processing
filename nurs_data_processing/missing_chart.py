"""
Tools for visualizing how missingness of a variable varies across a second variable.
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def metrics(data: pd.DataFrame, missing_col: str, feature_col: str, ci_width: float = 0.95):
    """
    Summarize the rate at which 'missing_col' is unfilled for a location of 'feature_col' using
     Bayesian 95% CI for the percentage missing.
    Returns a dictionary where "Missing", "Lower" and "Upper" reflect the proportion missing
    and "Feature" is the mode of data[feature_col] for categorical data and
    the mean of data[feature_col] otherwise.
    Bayesian analysis based on a Jeffrey's prior of a binomial distribution.
    Parameters
    ----------
    data: pandas.DataFrame
        The data set to summarize.
    missing_col: str
        The column to calculate missing CI from.
    feature_col: str
        The column to summarize as the feature.
    ci_width: float [0 < q < 1]
        Width of the CI.

    Returns
    -------
    dict("Feature", "Missing", "Lower", "Upper")
    """
    missing_sum = data[missing_col].isna().sum()
    n_cases, _ = data.shape

    a_star = 0.5 + missing_sum
    b_star = 0.5 + n_cases - missing_sum

    if data.dtypes[feature_col] == "object":
        result = {
            'Feature': data[feature_col].fillna("NaN").mode().values[0]
        }
    else:
        result = {
            'Feature': data[feature_col].mean()
        }
    alpha = (1 - ci_width) / 2
    result.update({
        'Missing': stats.beta.ppf(0.5, a_star, b_star),
        "Lower": stats.beta.ppf(0.5, a_star, b_star) - stats.beta.ppf(alpha, a_star, b_star),
        "Upper": stats.beta.ppf(1 - alpha, a_star, b_star) - stats.beta.ppf(0.5, a_star, b_star)
    })

    return result


def group_vector(data, column, n_bins=10):
    """
    Make a vector out of data[column] on which data can be grouped.
    If data[column] is categorical returns the values (having filled in missing values with "NaN")
    if data[column] is numeric returns q bins.
    Parameters
    ----------
    data: pd.DataFrame

    column: str
    n_bins: int [Optional]

    Returns
    -------

    """
    if data.dtypes[column] == "object":
        return data[column].fillna("NaN")

    return pd.qcut(data[column], q=n_bins)


def missing_chart(data, missing_col, feature_col):
    """
    Produce a visual representation of how the missing proportion of data[missing_col]
    varies across data[feature_col].  Can handle data[feature_col] being either numeric or
    categorical
    Parameters
    ----------
    data: pandas.DataFrame
    missing_col: str
    feature_col: str

    """
    group_by = group_vector(data, feature_col)
    summary = pd.DataFrame(
        {i: metrics(df, missing_col, feature_col) for i, df in data.groupby(group_by)}
    ).T

    plt.errorbar(
        summary["Feature"],
        summary["Missing"],
        yerr=summary[["Lower", "Upper"]].values.T
    )
    plt.hlines(
        metrics(data, missing_col, feature_col)["Missing"],
        xmin=min(summary["Feature"]),
        xmax=max(summary["Feature"]),
        linestyles="dashed"
    )


if __name__ == '__main__':
    f = pd.read_csv("cli/tests/test_data/missing_data.csv")

    missing_chart(f, "C", "A")
    plt.show()

    missing_chart(f, "C", "B")
    plt.show()

    missing_chart(f, "C", "D")
    plt.show()
