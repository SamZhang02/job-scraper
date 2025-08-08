import requests
from typing import Any, override
from datetime import datetime

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper


class JobPulseScraper(Scraper):

    def __init__(
        self,
        url: str = "https://job-pulse.uc.r.appspot.com/jobs/sde?yoe_less_than=1&page_number=1&page_size=99999",
    ) -> None:
        super().__init__()
        self.url: str = url

    def _fetch_url(self) -> list[dict[str, Any]]:
        response = requests.get(self.url)
        return response.json()

    def _convert_to_posting(self, posting: dict[str, Any]) -> JobPosting | None:
        date_str = posting["date_added"]

        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            return None

        timestamp = dt.timestamp()
        if not timestamp > 1748761200:
            return None

        link = posting["apply_link"] if posting["apply_link"] else posting["link"]

        return JobPosting(
            title=posting["title"],
            company=posting["company"],
            locations=posting["location"],
            url=link,
            source=self.get_source_name(),
            date_posted=timestamp,
        )

    @override
    def get_source_name(self) -> str:
        return "https://jobpulse.fyi/"

    def scrape(self) -> list[JobPosting]:
        response_json = self._fetch_url()
        postings = [self._convert_to_posting(obj) for obj in response_json]

        return [posting for posting in postings if posting is not None]
