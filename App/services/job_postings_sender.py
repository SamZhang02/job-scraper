import time
import os
import threading
import schedule

from collections.abc import Iterable
from typing import Any
from queue import Queue

from App.models.job_posting import JobPosting


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

    def _read_last_postings_state(self) -> set[str]:
        old_postings = []
        if not os.path.exists(self.persist_postings_path):
            return set()

        with open(self.persist_postings_path, "r") as fp:
            old_postings = set(fp.readlines())

        return old_postings

    def _persist_postings(self, postings: Iterable[JobPosting]) -> None:
        with open(self.persist_postings_path, "w") as fp:
            _ = fp.write("\n".join([str(posting) for posting in postings]))

    def _extract_new_postings(
        self, old_postings: Iterable[str], all_postings: Iterable[JobPosting]
    ):
        return [posting for posting in all_postings if str(posting) not in old_postings]

    def _send_postings(
        self,
        postings: Iterable[JobPosting],
    ):
        for posting in postings:
            self.channel.send(str(posting))

    def deduplicate_and_send_postings(self):
        all_postings = set()
        while not self.queue.empty():
            all_postings.add(self.queue.get())

        already_posted_postings = self._read_last_postings_state()
        new_postings = self._extract_new_postings(
            already_posted_postings, list(all_postings)
        )
        if new_postings:
            self._send_postings(new_postings)

        self._persist_postings(all_postings)

    def start_sender(self):
        schedule.every(self.interval_in_seconds).seconds.do(
            self.deduplicate_and_send_postings
        )

        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        print("Starting job posting sender...")
        thread = threading.Thread(target=self.start_sender, daemon=True)
        thread.start()
