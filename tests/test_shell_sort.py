import json,pytest
from sorting_visualizer import shell_sort,main

@pytest.mark.parametrize('values',[[],[1],[3,-1,3,0,2],list(range(100,0,-1))])
@pytest.mark.parametrize('reverse',[False,True])
def test_shell_sort_preserves_in_place_contract(values,reverse):
    original=values.copy();result=shell_sort(values,visualize=False,reverse=reverse)
    assert result is values and result==sorted(original,reverse=reverse)

def test_shell_sort_is_available_in_unattended_json(capsys):
    assert main(['--algorithm','shell','--values','3,1,2','--json'])==0
    assert json.loads(capsys.readouterr().out)=={'algorithm':'shell','values':[1,2,3]}
