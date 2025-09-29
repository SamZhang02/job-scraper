import os
import threading
import schedule
import asyncio
import logging

from collections.abc import Iterable
from typing import Any
from queue import Queue
from time import sleep

from App.models.job_posting import JobPosting
from App.util.job_posting_embedder import JobPostingEmbedder

logger = logging.getLogger("discord")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

POSTINGS_FILE = os.path.join(DATA_DIR, "postings.json")


class JobPostingsSender:
    def __init__(
        self,
        queue: Queue[JobPosting],
        interval_in_seconds: int,
        channel: Any,
        persist_postings_path: str = "postings",
    ) -> None:
        self.queue: Queue[JobPosting] = queue
        self.interval_in_seconds: int = interval_in_seconds
        self.channel: Any = channel
        self.persist_postings_path: str = persist_postings_path
        self.loop = asyncio.get_event_loop()

    def _read_last_postings_state(self) -> set[str]:
        old_postings = []
        if not os.path.exists(self.persist_postings_path):
            return set()

        with open(self.persist_postings_path, "r") as fp:
            old_postings = set([line.strip() for line in fp.readlines()])

        return old_postings

    def _persist_postings(self, postings: Iterable[JobPosting]) -> None:
        with open(self.persist_postings_path, "w") as fp:
            _ = fp.write("\n".join([str(posting) for posting in postings]))

    def _extract_new_postings(
        self, old_postings: Iterable[str], all_postings: Iterable[JobPosting]
    ):
        new_postings = [
            posting for posting in all_postings if str(posting) not in old_postings
        ]
        logger.info(f"Got {len(new_postings)} new postings")

        return new_postings

    async def _send_postings(
        self,
        postings: Iterable[JobPosting],
    ):
        for posting in postings:
            embed = JobPostingEmbedder.embed(posting)
            await self.channel.send(embed=embed)
            sleep(0.1)  # Prevent rate limit

    async def deduplicate_and_send_postings(self):
        all_postings = set()
        while not self.queue.empty():
            all_postings.add(self.queue.get())

        already_posted_postings = self._read_last_postings_state()
        new_postings = self._extract_new_postings(
            already_posted_postings, list(all_postings)
        )

        self._persist_postings(all_postings)

        if new_postings:
            await self._send_postings(new_postings)

    def start_sender(self):
        schedule.every(self.interval_in_seconds).seconds.do(
            lambda: asyncio.run_coroutine_threadsafe(
                self.deduplicate_and_send_postings(), self.loop
            )
        )

    def run(self):
        logger.info("Starting job posting sender...")
        thread = threading.Thread(target=self.start_sender, daemon=True)
        thread.start()
