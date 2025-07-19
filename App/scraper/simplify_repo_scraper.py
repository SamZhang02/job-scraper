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
        if not self._is_2026_ng_posting(posting):
            return None

        return JobPosting(
            title=posting["title"],
            company=posting["company_name"],
            locations=", ".join(posting["locations"]),
            url=posting["url"],
            source=self.get_source_name(),
        )

    @override
    def get_source_name(self) -> str:
        return "https://github.com/SimplifyJobs/New-Grad-Positions"

    @override
    def scrape(self) -> list[JobPosting]:
        response_json = self._fetch_url()
        postings = [self._convert_to_posting(obj) for obj in response_json]

        return [posting for posting in postings if posting is not None]

    def _is_2026_ng_posting(self, posting: dict[str, Any]) -> bool:
        return posting["active"] and posting["date_posted"] > 1748761200


if __name__ == "__main__":
    scraper = SimplifyRepoScraper()
    scraper.scrape()
