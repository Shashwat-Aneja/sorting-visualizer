import json
import pytest
from sorting_visualizer import counting_sort, main

@pytest.mark.parametrize('values',[[],[-2,3,-2,0],[5,5,5]])
@pytest.mark.parametrize('reverse',[False,True])
def test_integer_counting_sort(values,reverse):
    original=values.copy();result=counting_sort(values,visualize=False,reverse=reverse)
    assert result is values and result==sorted(original,reverse=reverse)

def test_range_bound_and_cli(capsys):
    with pytest.raises(ValueError,match='span'):counting_sort([0,1000001],visualize=False)
    assert main(['--algorithm','counting','--values','3,-1,3','--json'])==0
    assert json.loads(capsys.readouterr().out)['values']==[-1,3,3]


@pytest.mark.parametrize("json_mode", [False, True])
def test_counting_span_cli_has_usage_error_not_traceback(json_mode,capsys):
    args=['--algorithm','counting','--values','0,1000001','--no-visualization']+(['--json'] if json_mode else [])
    with pytest.raises(SystemExit) as exc:main(args)
    assert exc.value.code==2
    captured=capsys.readouterr()
    assert 'span' in captured.err and 'Traceback' not in captured.err
