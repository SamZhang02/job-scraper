import time
import threading
from queue import Queue, Empty
from typing import override
import pytest

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper
from App.scraper.scraper_manager import ScraperManager


class DummyScraper1(Scraper):
    @override
    def get_source_name(self):
        return "DummySource1"

    @override
    def scrape(self):
        return [JobPosting("job 1", "company", "NYC, NJ", "url", "source")]


class DummyScraper2(Scraper):
    @override
    def get_source_name(self):
        return "DummySource2"

    @override
    def scrape(self):
        return [
            JobPosting("job 2", "company", "NYC", "url", "source"),
            JobPosting("job 3", "company", "SF", "url", "source"),
        ]


def test_scraper_manager_integration():
    queue: Queue[JobPosting] = Queue()
    scraper1 = DummyScraper1()
    scraper2 = DummyScraper2()

    manager = ScraperManager(
        scrapers=[scraper1, scraper2],
        interval_in_seconds=2,
        queue=queue,
    )

    manager.run()

    # Wait for at least one scrape cycle
    time.sleep(4)

    collected = []
    try:
        while True:
            collected.append(queue.get_nowait())
    except Empty:
        pass

    titles = collected

    assert JobPosting("job 1", "company", "NYC, NJ", "url", "source") in titles
    assert JobPosting("job 2", "company", "NYC", "url", "source") in titles
    assert JobPosting("job 3", "company", "SF", "url", "source") in titles
