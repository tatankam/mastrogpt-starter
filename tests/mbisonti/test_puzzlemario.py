import sys 
sys.path.append("packages/mbisonti/puzzlemario")
import puzzlemario

def test_puzzlemario():
    res = puzzlemario.puzzlemario({})
    assert res["output"] == "puzzlemario"
