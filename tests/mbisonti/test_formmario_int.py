import os, requests as req
def test_formmario():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/mbisonti/formmario"
    res = req.get(url).json()
    assert res.get("output") == "formmario"
