import sorting_visualizer as app

def test_frame_budget_caps_rendering_but_not_sorting(capsys,monkeypatch):
    frames=[];monkeypatch.setattr(app,'print_array',lambda arr,**kwargs:frames.append(list(arr)));monkeypatch.setattr(app.time,'sleep',lambda value:None)
    assert app.main(['--algorithm','bubble','--values','4,3,2,1','--max-frames','2'])==0
    assert len(frames)==2 and '[1, 2, 3, 4]' in capsys.readouterr().out
    assert app.FRAME_BUDGET.get() is None

def test_zero_frame_budget_disables_animation_clear(monkeypatch):
    def unexpected(*args,**kwargs):raise AssertionError('animation used')
    monkeypatch.setattr(app,'clear_console',unexpected);monkeypatch.setattr(app.time,'sleep',unexpected)
    assert app.main(['--algorithm','heap','--values','2,1','--max-frames','0'])==0
