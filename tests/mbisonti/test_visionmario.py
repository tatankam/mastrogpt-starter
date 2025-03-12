import sys 
sys.path.append("packages/mbisonti/visionmario")
import visionmario

def test_visionmario():
    res = visionmario.visionmario({})
    assert res["output"] == "visionmario"
