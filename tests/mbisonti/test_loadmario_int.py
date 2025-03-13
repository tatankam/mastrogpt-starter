import os, requests as req
def test_loadmario():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/mbisonti/loadmario"
    res = req.get(url).json()
    assert res.get("output") == "loadmario"
