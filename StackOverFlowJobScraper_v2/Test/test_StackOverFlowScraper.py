from .. import StackOverFlowScraper
import pytest


#tests getUrl function successfully grabs url
def test_get_url():
    assert StackOverFlowScraper.get_url() is not None


#tests for internet connection, code that is not 200 mean's it can't connect
def test_internet_connection():
    url = "https://stackoverflow.com/jobs/feed?location=bridgewater&range=50&distanceUnits=Miles"
    resp = StackOverFlowScraper.requests.get(url)
    assert resp.status_code is 200


#tests that program exits gracefully if url is mispelled (this won't happen in the actual program but Tests!)
def test_bad_url():
    url = "https://stackoberflow.com/jobs/feed?location=bridgewater&range=50&distanceUnits=Miles"
    with pytest.raises(Exception):
        StackOverFlowScraper.requests.get(url)

