import os, requests as req
def test_visionmario():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/visionmario/visionmario"
    res = req.get(url).json()
    assert res.get("output") == "visionmario"
