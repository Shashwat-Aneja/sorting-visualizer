from sorting_visualizer import bubble_sort, insertion_sort, selection_sort


SORTERS = (bubble_sort, insertion_sort, selection_sort)


def test_sorters_order_unsorted_values_without_visualization():
    for sorter in SORTERS:
        assert sorter([5, 1, 4, 2, 8], visualize=False) == [1, 2, 4, 5, 8]


def test_sorters_handle_empty_and_single_item_lists():
    for sorter in SORTERS:
        assert sorter([], visualize=False) == []
        assert sorter([7], visualize=False) == [7]


def test_sorters_preserve_duplicate_values():
    for sorter in SORTERS:
        assert sorter([3, 1, 3, 2, 1], visualize=False) == [1, 1, 2, 3, 3]
