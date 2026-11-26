import pytest
import sorting_visualizer as app

def test_value_count_budget_precedes_integer_conversion(monkeypatch):
    monkeypatch.setattr(app,'MAX_INPUT_VALUES',2)
    with pytest.raises(ValueError,match='value budget'):app.parse_values('1,2,3')

def test_file_byte_budget_preserves_source_and_output(tmp_path,monkeypatch):
    source=tmp_path/'in.txt';source.write_text('1 2 3 4');out=tmp_path/'out.json';out.write_text('keep')
    monkeypatch.setattr(app,'MAX_INPUT_BYTES',4)
    with pytest.raises(SystemExit):app.main(['--algorithm','quick','--values-file',str(source),'--output',str(out)])
    assert source.read_text()=='1 2 3 4' and out.read_text()=='keep'
