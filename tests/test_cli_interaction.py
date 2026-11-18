"""CLI regression tests for interactive and automated invocation."""

import builtins

import pytest

from sorting_visualizer import main


def test_interactive_eof_reports_usage_without_traceback(monkeypatch, capsys):
    def closed_stdin(_prompt):
        raise EOFError

    monkeypatch.setattr(builtins, "input", closed_stdin)
    assert main(["--no-visualization"]) == 2
    assert "Use --algorithm" in capsys.readouterr().out


def test_interactive_choice_accepts_surrounding_whitespace(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _prompt: " 1  ")
    assert main(["--values", "3,1,2", "--no-visualization"]) == 0
    assert "[1, 2, 3]" in capsys.readouterr().out


def test_noninteractive_choice_does_not_read_stdin(monkeypatch, capsys):
    def unexpected_input(_prompt):
        pytest.fail("non-interactive mode must not read stdin")

    monkeypatch.setattr(builtins, "input", unexpected_input)
    assert main(["--algorithm", "quick", "--values", "2,1", "--no-visualization"]) == 0
    assert "[1, 2]" in capsys.readouterr().out
