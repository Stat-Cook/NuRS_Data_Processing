"""
Plotting tools for summarizing categorical data with a large numbers of values.
"""
from textwrap import TextWrapper
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import container  # pylint: disable=unused-import
import numpy as np

WRAPPER = TextWrapper(width=30, max_lines=2)


def common_bar_chart(counter: Counter, k: int = 10):
    """
    Produces a bar chart of the k most common classes
    plus a catch all for rarer classes.
    Parameters
    ----------
    counter: Counter
    k: int [optional]

    Returns
    -------
    container.BarContainer
    """
    items = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    if len(items) > k:
        other_total = sum(val for _, val in items[k:])
        items = items[:k]
        items.append(("Other", other_total))

    names, values = np.transpose(items)

    names = ["\n".join(WRAPPER.wrap(i)) for i in names]
    values = [float(i) for i in values]

    return plt.bar(names, values)
