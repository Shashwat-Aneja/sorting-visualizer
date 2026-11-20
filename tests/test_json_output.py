import json,pytest
import sorting_visualizer as app
def test_json_mode_is_clean_and_unanimated(capsys,monkeypatch):
    monkeypatch.setattr(app.time,'sleep',lambda _:pytest.fail('animation delay'))
    assert app.main(['--algorithm','quick','--values','3,-1,3','--json'])==0
    assert json.loads(capsys.readouterr().out)=={'algorithm':'quick','values':[-1,3,3]}
def test_json_requires_explicit_algorithm():
    with pytest.raises(SystemExit):app.main(['--json'])
