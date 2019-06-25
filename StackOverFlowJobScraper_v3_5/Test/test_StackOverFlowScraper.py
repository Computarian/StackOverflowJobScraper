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


#tests that map appears with good data
def test_basemap_with_good_data():
    cities = ["Boston, MA"]
    assert StackOverFlowScraper.basemap(cities) is not None


#tests that map appears with bad data
def test_basemap_with_bad_data():
    cities = ["hello"]
    assert StackOverFlowScraper.basemap(cities) is not None


#tests that garbage keyword doesn't break program
def test_web_scraper_with_bad_keyword():
    keyword = "Raaaaaaaaaaaaaaaaaaaaaaaaaaaarggghh Tkinter Canvas makes me mad!!"
    assert StackOverFlowScraper.web_scraper(keyword) is not None

