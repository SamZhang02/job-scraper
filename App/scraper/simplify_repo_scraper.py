from typing import Any

import requests

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper
from App.util.typing_compat import override

BLOCKED_COMPANIES = {
    "https://simplify.jobs/c/Jerry",
}

INCLUSION_TERMS = {
    "software eng",
    "software dev",
    "product engineer",
    "fullstack engineer",
    "frontend",
    "front end",
    "front-end",
    "backend",
    "back end",
    "full-stack",
    "full stack",
    "founding engineer",
    "mobile dev",
    "mobile engineer",
    "data scientist",
    "data engineer",
    "research eng",
    "product manag",
    "apm",
    "product",
    "devops",
    "android",
    "ios",
    "sre",
    "site reliability eng",
    "quantitative trad",
    "quantitative research",
    "quantitative dev",
    "security eng",
    "compiler eng",
    "machine learning eng",
    "hardware eng",
    "firmware eng",
    "infrastructure eng",
    "embedded",
    "fpga",
    "circuit",
    "chip",
    "silicon",
    "asic",
    "quant",
    "quantitative",
    "trading",
    "finance",
    "investment",
    "ai &",
    "machine learning",
    "ml",
    "analytics",
    "analyst",
    "research sci",
    "engineer",
    "developer",
}

NEW_GRAD_TERMS = {
    "new grad",
    "early career",
    "college grad",
    "entry level",
    "entry-level",
    "founding",
    "early in career",
    "university grad",
    "fresh grad",
    "recent grad",
    "2024 grad",
    "2025 grad",
    "2026 grad",
    "engineer 0",
    "engineer 1",
    "engineer i",
    "junior",
    "sde 1",
    "sde i",
    "grad",
}


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
            date_posted=float(posting["date_posted"]),
        )

    def _is_2026_ng_posting(self, posting: dict[str, Any]) -> bool:
        if not (posting.get("active") and posting.get("date_posted") and posting["date_posted"] > 1748761200):
            return False

        if self._is_blocked_company(posting):
            return False

        search_blob = self._build_search_blob(posting)

        has_role_match = any(term in search_blob for term in INCLUSION_TERMS)
        has_new_grad_match = any(term in search_blob for term in NEW_GRAD_TERMS)

        return has_role_match and has_new_grad_match

    def _is_blocked_company(self, posting: dict[str, Any]) -> bool:
        company_url = posting.get("company_url") or posting.get("url")
        return company_url in BLOCKED_COMPANIES if company_url else False

    def _build_search_blob(self, posting: dict[str, Any]) -> str:
        values: list[str] = []
        fields = [
            posting.get("title", ""),
            posting.get("description", ""),
            posting.get("team", ""),
            posting.get("job_type", ""),
            " ".join(posting.get("job_types", [])),
            " ".join(posting.get("locations", [])),
            " ".join(posting.get("tags", [])),
        ]
        for value in fields:
            if value:
                values.append(value)

        return " ".join(values).lower()

    @override
    def get_source_name(self) -> str:
        return "https://github.com/SimplifyJobs/New-Grad-Positions"

    @override
    def scrape(self) -> list[JobPosting]:
        response_json = self._fetch_url()
        postings = [self._convert_to_posting(obj) for obj in response_json]

        return [posting for posting in postings if posting is not None]


if __name__ == "__main__":
    scraper = SimplifyRepoScraper()
    scraper.scrape()
