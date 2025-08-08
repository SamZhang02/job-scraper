from __future__ import annotations

from dataclasses import dataclass
from typing import override

PosixTime = float


@dataclass(frozen=True)
class JobPosting:
    title: str
    company: str
    locations: str
    url: str
    source: str
    date_posted: PosixTime

    @override
    def __str__(self) -> str:
        return f"JobPosting(title={self.title}, company={self.company}, date_posted={self.date_posted})"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JobPosting):
            return False

        return (
            self.title == other.title
            and self.company == other.company
            and self.date_posted == other.date_posted
        )
