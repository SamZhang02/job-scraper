from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class JobPosting:
    title: str
    company: str
    locations: str
    url: str
    source: str
