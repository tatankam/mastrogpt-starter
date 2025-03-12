import sys 
sys.path.append("packages/mbisonti/formmario")
import formmario

def test_formmario():
    res = formmario.formmario({})
    assert res["output"] == "formmario"
