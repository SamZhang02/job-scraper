from queue import Queue
import threading
from App.models.job_posting import JobPosting
import schedule
import time

from App.scraper.scraper import Scraper


class ScraperManager:
    def __init__(
        self,
        scrapers: list[Scraper],
        interval_in_seconds: int,
        queue: Queue[JobPosting],
    ):
        self.scrapers: list[Scraper] = scrapers
        self.interval_in_seconds: int = interval_in_seconds
        self.queue: Queue[JobPosting] = queue

    def scrape_job(self):
        for scraper in self.scrapers:
            print(f"Running scraper for {scraper.get_source_name()}")
            scraped_postings = scraper.scrape()
            for posting in scraped_postings:
                self.queue.put(posting)

    def start_scheduler(self):
        schedule.every(self.interval_in_seconds).seconds.do(self.scrape_job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        print("Starting scraper manager now.")
        thread = threading.Thread(target=self.start_scheduler, daemon=True)
        thread.start()
