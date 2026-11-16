"""Regression coverage for signed values and mutation contracts.

These cases exercise algorithm behavior independently of terminal rendering.
"""

import pytest

from sorting_visualizer import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


@pytest.mark.parametrize(
    "sorter",
    [bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort],
)
@pytest.mark.parametrize(
    "values",
    [
        [0, -1, -1, 0, 1],
        [10**30, -(10**30), 2, -(10**30), 10**30],
        list(range(30, -31, -1)),
        [7] * 100,
    ],
)
def test_sorters_preserve_identity_and_match_builtin_sorted(sorter, values):
    original = values.copy()
    result = sorter(values, visualize=False)

    assert result is values
    assert values == sorted(original)
    assert len(values) == len(original)
