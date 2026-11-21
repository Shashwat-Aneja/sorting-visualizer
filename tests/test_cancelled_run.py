import sorting_visualizer as app
def test_keyboard_interrupt_at_prompt_returns_conventional_status(monkeypatch,capsys):
    def cancel(*args):raise KeyboardInterrupt
    monkeypatch.setattr('builtins.input',cancel)
    assert app.main([])==130
    assert 'Sorting interrupted' in capsys.readouterr().err
def test_keyboard_interrupt_during_sort_returns_status_without_traceback(monkeypatch):
    def cancel(*args,**kwargs):raise KeyboardInterrupt
    monkeypatch.setattr(app,'bubble_sort',cancel)
    assert app.main(['--algorithm','bubble','--no-visualization'])==130
