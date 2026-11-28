import json
from sorting_visualizer import main

def test_distinct_cli_from_file_and_descending(tmp_path,capsys):
    source=tmp_path/'v.txt';source.write_text('3 1 3 2 1')
    assert main(['--algorithm','merge','--values-file',str(source),'--unique','--descending','--json'])==0
    data=json.loads(capsys.readouterr().out)
    assert data['values']==[3,2,1] and data['input_count']==5 and data['unique_count']==3
