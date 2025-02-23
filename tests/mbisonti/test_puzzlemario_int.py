import os, requests as req
def test_puzzlemario():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/mbisonti/puzzlemario"
    res = req.get(url).json()
    assert res.get("output") == "puzzlemario"
