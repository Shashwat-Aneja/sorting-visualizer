import pytest,json
from sorting_visualizer import heap_sort,main
@pytest.mark.parametrize('values',[[],[1],[3,-1,3,0],list(range(100)),list(range(100,0,-1))])
@pytest.mark.parametrize('reverse',[False,True])
def test_heap_sort_contract(values,reverse):
    expected=sorted(values,reverse=reverse)
    assert heap_sort(values,visualize=False,reverse=reverse) is values
    assert values==expected
def test_heap_cli_json_and_descending(capsys):
    assert main(['--algorithm','heap','--values','2,1,3','--descending','--json'])==0
    assert json.loads(capsys.readouterr().out)['values']==[3,2,1]
