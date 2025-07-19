from abc import ABC

from App.models.job_posting import JobPosting


class Scraper(ABC):
    def get_source_name(self) -> str: ...

    def scrape(self) -> list[JobPosting]: ...
