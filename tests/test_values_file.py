import json,pytest
from sorting_visualizer import main
def test_file_values_support_multiline_and_comma_separators(tmp_path,capsys):
    p=tmp_path/'values.txt';p.write_text('3, -1\n2 2\n')
    assert main(['--values-file',str(p),'--algorithm','heap','--json'])==0
    assert json.loads(capsys.readouterr().out)['values']==[-1,2,2,3]
def test_file_and_inline_inputs_are_mutually_exclusive(tmp_path):
    with pytest.raises(SystemExit):main(['--values-file',str(tmp_path/'x'),'--values','1,2'])
def test_missing_input_file_has_controlled_cli_failure(tmp_path):
    with pytest.raises(SystemExit) as exc:main(['--values-file',str(tmp_path/'missing'),'--algorithm','heap'])
    assert exc.value.code==2
