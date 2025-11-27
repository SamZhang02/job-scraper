import time
import threading
from queue import Queue, Empty

import pytest

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper
from App.scraper.scraper_manager import ScraperManager
from App.util.typing_compat import override


NOW = 1_750_000_000.0


class DummyScraper1(Scraper):
    @override
    def get_source_name(self):
        return "DummySource1"

    @override
    def scrape(self):
        return [
            JobPosting(
                "job 1",
                "company",
                "NYC, NJ",
                "url",
                "source",
                NOW,
            )
        ]


class DummyScraper2(Scraper):
    @override
    def get_source_name(self):
        return "DummySource2"

    @override
    def scrape(self):
        return [
            JobPosting("job 2", "company", "NYC", "url", "source", NOW),
            JobPosting("job 3", "company", "SF", "url", "source", NOW),
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

    assert JobPosting("job 1", "company", "NYC, NJ", "url", "source", NOW) in titles
    assert JobPosting("job 2", "company", "NYC", "url", "source", NOW) in titles
    assert JobPosting("job 3", "company", "SF", "url", "source", NOW) in titles
