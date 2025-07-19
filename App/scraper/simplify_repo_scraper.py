from typing import Any, override
import requests

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper


class SimplifyRepoScraper(Scraper):

    def __init__(
        self,
        url: str = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/refs/heads/dev/.github/scripts/listings.json",
    ) -> None:
        super().__init__()
        self.url: str = url

    def _fetch_url(self) -> list[dict[str, Any]]:
        response = requests.get(self.url)
        return response.json()

    def _convert_to_posting(self, posting: dict[str, Any]) -> JobPosting | None:
        if not posting["active"]:
            return None

        return JobPosting(
            title=posting["title"],
            company=posting["company_name"],
            locations=posting["locations"],
            url=posting["url"],
            source=self.get_source_name(),
        )

    @override
    def get_source_name(self) -> str:
        return "Simplify Repo"

    @override
    def scrape(self) -> list[JobPosting]:
        response_json = self._fetch_url()
        postings = [self._convert_to_posting(obj) for obj in response_json]

        return [posting for posting in postings if posting is not None]


if __name__ == "__main__":
    scraper = SimplifyRepoScraper()
    scraper.scrape()
