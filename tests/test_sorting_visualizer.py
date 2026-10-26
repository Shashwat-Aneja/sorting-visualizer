from sorting_visualizer import bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort


SORTERS = (bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort)


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


def test_bubble_sort_stops_after_an_already_sorted_pass(monkeypatch):
    import sorting_visualizer

    comparisons = []
    monkeypatch.setattr(
        sorting_visualizer,
        "render_step",
        lambda arr, message, enabled: comparisons.append(message),
    )

    assert sorting_visualizer.bubble_sort([1, 2, 3, 4], visualize=False) == [1, 2, 3, 4]
    assert len(comparisons) == 3


def test_parse_values_accepts_comma_separated_integers():
    from sorting_visualizer import parse_values

    assert parse_values(" 9, -2, 4 ") == [9, -2, 4]


def test_parse_values_rejects_empty_or_non_integer_values():
    import pytest
    from sorting_visualizer import parse_values

    with pytest.raises(ValueError):
        parse_values("1,,3")
    with pytest.raises(ValueError):
        parse_values("1,two,3")


def test_cli_can_sort_custom_values_without_animation(monkeypatch, capsys):
    import sorting_visualizer

    monkeypatch.setattr("builtins.input", lambda _prompt: "1")
    monkeypatch.setattr(sorting_visualizer.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(sorting_visualizer, "clear_console", lambda: None)

    sorting_visualizer.main(["--values", "3,1,2", "--no-visualization"])

    assert "[1, 2, 3]" in capsys.readouterr().out


def test_merge_sort_mutates_the_supplied_list():
    values = [9, -1, 4, 4, 0]

    result = merge_sort(values, visualize=False)

    assert result is values
    assert values == [-1, 0, 4, 4, 9]


def test_cli_lists_merge_sort(monkeypatch, capsys):
    import sorting_visualizer

    monkeypatch.setattr("builtins.input", lambda _prompt: "4")
    monkeypatch.setattr(sorting_visualizer.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(sorting_visualizer, "clear_console", lambda: None)

    sorting_visualizer.main(["--values", "3,1,2", "--no-visualization"])

    output = capsys.readouterr().out
    assert "4. Merge Sort" in output
    assert "[1, 2, 3]" in output


def test_quick_sort_handles_large_duplicate_heavy_and_negative_inputs():
    values = [((index * 17) % 23) - 11 for index in range(2500)]
    values.extend([0] * 300)
    expected = sorted(values)

    result = quick_sort(values, visualize=False)

    assert result is values
    assert values == expected


def test_quick_sort_cli_choice_is_available(monkeypatch, capsys):
    import sorting_visualizer

    monkeypatch.setattr("builtins.input", lambda _prompt: "5")
    monkeypatch.setattr(sorting_visualizer.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(sorting_visualizer, "clear_console", lambda: None)

    sorting_visualizer.main(["--values", "3,-1,3,0", "--no-visualization"])

    output = capsys.readouterr().out
    assert "5. Quick Sort" in output
    assert "[-1, 0, 3, 3]" in output


def test_cli_runs_named_algorithm_without_prompt(monkeypatch, capsys):
    import sorting_visualizer

    def fail_prompt(_prompt):
        raise AssertionError("named algorithm selection must not prompt")

    monkeypatch.setattr("builtins.input", fail_prompt)
    monkeypatch.setattr(sorting_visualizer.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(sorting_visualizer, "clear_console", lambda: None)

    sorting_visualizer.main(
        ["--algorithm", "quick", "--values", "3,-1,3,0", "--no-visualization"]
    )

    output = capsys.readouterr().out
    assert "Running Quick Sort" in output
    assert "[-1, 0, 3, 3]" in output
