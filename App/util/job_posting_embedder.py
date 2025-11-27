from datetime import datetime, timezone

from discord import Embed

from App.models.job_posting import JobPosting

FAANG_PLUS = {
    "airbnb",
    "adobe",
    "amazon",
    "amd",
    "anthropic",
    "apple",
    "asana",
    "atlassian",
    "bytedance",
    "cloudflare",
    "coinbase",
    "crowdstrike",
    "databricks",
    "datadog",
    "doordash",
    "dropbox",
    "duolingo",
    "figma",
    "google",
    "ibm",
    "instacart",
    "intel",
    "linkedin",
    "lyft",
    "meta",
    "microsoft",
    "netflix",
    "notion",
    "nvidia",
    "openai",
    "oracle",
    "palantir",
    "paypal",
    "perplexity",
    "pinterest",
    "ramp",
    "reddit",
    "rippling",
    "robinhood",
    "roblox",
    "salesforce",
    "samsara",
    "servicenow",
    "shopify",
    "slack",
    "snap",
    "snapchat",
    "spacex",
    "splunk",
    "snowflake",
    "stripe",
    "square",
    "tesla",
    "tinder",
    "tiktok",
    "uber",
    "visa",
    "waymo",
    "x",
}


class JobPostingEmbedder:

    @staticmethod
    def _format_company(posting: JobPosting) -> str:
        company = posting.company
        if company and company.strip().lower() in FAANG_PLUS:
            return f"🔥 @All {company}"
        return company

    @staticmethod
    def _format_date(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    @staticmethod
    def embed(posting: JobPosting) -> Embed:
        company_value = JobPostingEmbedder._format_company(posting)
        date_posted_value = JobPostingEmbedder._format_date(posting.date_posted)
        return (
            Embed(
                title=posting.title,
                url=posting.url,
            )
            .add_field(name="Company", value=company_value, inline=False)
            .add_field(name="Locations", value=posting.locations, inline=False)
            .add_field(name="Source", value=posting.source, inline=False)
            .add_field(name="Date Posted", value=date_posted_value, inline=False)
        )
