import pytest
import sorting_visualizer as app
def test_cli_frame_delay_is_applied_and_restored(monkeypatch):
    sleeps=[];monkeypatch.setattr(app.time,'sleep',sleeps.append);monkeypatch.setattr(app,'clear_console',lambda:None)
    assert app.main(['--algorithm','bubble','--values','2,1','--delay','0.01'])==0
    assert .01 in sleeps and app.FRAME_DELAY.get()==.2
@pytest.mark.parametrize('value',['-1','nan','inf','11'])
def test_invalid_animation_delay_is_rejected(value):
    with pytest.raises(SystemExit):app.main(['--delay',value])
