import sys 
sys.path.append("packages/mbisonti/loadmario")
import loadmario

def test_loadmario():
    res = loadmario.loadmario({})
    assert res["output"] == "loadmario"
