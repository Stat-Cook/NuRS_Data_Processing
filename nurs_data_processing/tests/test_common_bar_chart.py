from ..common_bar_chart import common_bar_chart
from collections import Counter


def test_small_bar_chart():
    counter = Counter(list("ABABAABBBAABABAABAAA"))
    plt = common_bar_chart(counter)
    assert len(plt.patches) == 2


def test_large_bar_chart():
    counter = Counter(list("ABCDEFGHIJKLMNOPQRST"))
    plt = common_bar_chart(counter)
    assert len(plt.patches) == 11


def test_large_bar_chart_k_6():
    counter = Counter(list("ABCDEFGHIJKLMNOPQRST"))
    k = 5
    plt = common_bar_chart(counter, k=k)
    target = min(len(counter), k + 1)
    assert len(plt.patches) == target


def test_large_bar_chart_k_50():
    counter = Counter(list("ABCDEFGHIJKLMNOPQRST"))
    k = 50
    plt = common_bar_chart(counter, k=k)
    target = min(len(counter), k + 1)
    assert len(plt.patches) == target
