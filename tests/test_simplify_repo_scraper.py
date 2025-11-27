from typing import Any

from App.scraper.simplify_repo_scraper import SimplifyRepoScraper


def make_posting(**overrides: Any) -> dict[str, Any]:
    posting = {
        "title": "New Grad Software Engineer",
        "description": "New grad opportunity building trading systems",
        "team": "Engineering",
        "job_type": "Full-time",
        "job_types": ["Full-time"],
        "locations": ["Remote"],
        "tags": ["software"],
        "company_name": "Acme",
        "url": "https://simplify.jobs/p/acme",
        "company_url": "https://simplify.jobs/c/Acme",
        "active": True,
        "date_posted": 1_748_800_001,
    }
    posting.update(overrides)
    return posting


def test_simplify_scraper_filters_blocked_company(monkeypatch):
    scraper = SimplifyRepoScraper()
    blocked_posting = make_posting(company_url="https://simplify.jobs/c/Jerry")

    monkeypatch.setattr(scraper, "_fetch_url", lambda: [blocked_posting])

    assert scraper.scrape() == []


def test_simplify_scraper_requires_new_grad_terms(monkeypatch):
    scraper = SimplifyRepoScraper()
    posting = make_posting(
        title="Software Engineer",
        description="Work on infrastructure systems",
    )

    # Remove any text that would count as a new grad signal
    posting["tags"] = ["software", "backend"]

    monkeypatch.setattr(scraper, "_fetch_url", lambda: [posting])

    assert scraper.scrape() == []


def test_simplify_scraper_accepts_valid_new_grad_posting(monkeypatch):
    scraper = SimplifyRepoScraper()
    posting = make_posting(
        title="Software Engineer",
        description="Entry level engineer role",
        tags=["software", "entry level"],
    )

    monkeypatch.setattr(scraper, "_fetch_url", lambda: [posting])

    results = scraper.scrape()

    assert len(results) == 1
    assert results[0].title == "Software Engineer"
    assert results[0].company == "Acme"
