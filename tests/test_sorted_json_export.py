import json,pytest
from sorting_visualizer import main

def test_sorted_file_export_matches_json_output_and_preserves_input(tmp_path,capsys):
    source=tmp_path/'values.txt';source.write_text('3 1 2');out=tmp_path/'sorted.json'
    assert main(['--values-file',str(source),'--algorithm','heap','--output',str(out)])==0
    assert json.loads(out.read_text())==json.loads(capsys.readouterr().out)=={'algorithm':'heap','values':[1,2,3]}
    assert source.read_text()=='3 1 2'
    with pytest.raises(SystemExit):main(['--values-file',str(source),'--algorithm','heap','--output',str(source)])
    assert source.read_text()=='3 1 2'

def test_cleanup_supports_python37_unlink_signature(tmp_path,monkeypatch,capsys):
    import sorting_visualizer as app
    from pathlib import Path
    class LegacyPath(type(Path())):
        def unlink(self):return super().unlink()
    monkeypatch.setattr(app,'Path',LegacyPath)
    out=tmp_path/'out.json'
    assert main(['--algorithm','shell','--values','2,1','--output',str(out)])==0
    assert json.loads(out.read_text())['values']==[1,2]

def test_failed_sorted_json_replace_preserves_existing_output(tmp_path,monkeypatch):
    import sorting_visualizer as app
    out=tmp_path/'out.json';out.write_text('keep')
    def fail(*args):raise OSError('disk failure')
    monkeypatch.setattr(app.os,'replace',fail)
    with pytest.raises(OSError):app.export_sorted_json({'values':[1]},out)
    assert out.read_text()=='keep' and list(tmp_path.iterdir())==[out]
