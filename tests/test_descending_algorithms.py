import pytest,json
import sorting_visualizer as app
@pytest.mark.parametrize('algorithm',[app.bubble_sort,app.insertion_sort,app.selection_sort,app.merge_sort,app.quick_sort])
def test_each_algorithm_sorts_descending_in_place(algorithm):
    values=[-2,3,3,0,8,-1];result=algorithm(values,visualize=False,reverse=True)
    assert result is values and values==[8,3,3,0,-1,-2]
def test_json_descending_cli(capsys):
    assert app.main(['--algorithm','merge','--values','1,3,2','--json','--descending'])==0
    assert json.loads(capsys.readouterr().out)['values']==[3,2,1]
