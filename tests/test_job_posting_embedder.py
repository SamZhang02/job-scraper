from App.models.job_posting import JobPosting
from App.util.job_posting_embedder import JobPostingEmbedder


def _field(embed, name: str):
    for field in embed.fields:
        if field.name == name:
            return field
    raise AssertionError(f"Field {name} not found")


def test_embedder_formats_faang_company_and_date():
    posting = JobPosting(
        title="Software Engineer",
        company="Google",
        locations="Remote",
        url="https://careers.google/jobs/123",
        source="google",
        date_posted=1_710_000_000,
    )

    embed = JobPostingEmbedder.embed(posting)

    company_field = _field(embed, "Company")
    date_field = _field(embed, "Date Posted")

    assert company_field.value.startswith("🔥 @All")
    assert "Google" in company_field.value
    assert date_field.value == "2024-03-09"


def test_embedder_handles_non_faang_company():
    posting = JobPosting(
        title="Product Analyst",
        company="Acme",
        locations="Remote",
        url="https://acme.example/jobs/456",
        source="acme",
        date_posted=1_720_000_000,
    )

    embed = JobPostingEmbedder.embed(posting)

    company_field = _field(embed, "Company")
    date_field = _field(embed, "Date Posted")

    assert company_field.value == "Acme"
    assert date_field.value == "2024-07-03"
