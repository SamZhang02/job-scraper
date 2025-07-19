import pytest
import time
import threading
from queue import Queue
from unittest.mock import MagicMock

from App.services.job_postings_sender import JobPostingsSender
from App.models.job_posting import JobPosting


def dummy_posting(title: str):
    return JobPosting(title, "company", "location", "www.url.com", "src")


def test_job_postings_sender_input_output():
    queue: Queue[JobPosting] = Queue()
    channel = MagicMock()

    sender = JobPostingsSender(
        queue=queue,
        interval_in_seconds=2,
        channel=channel,
        persist_postings_path="ignore_this.txt",  # not tested
    )

    sender.run()

    queue.put(dummy_posting("JobA"))
    time.sleep(4)

    queue.put(dummy_posting("JobA"))  # should be ignored
    queue.put(dummy_posting("JobB"))  # should be sent
    time.sleep(1)

    sent = [call[0][0] for call in channel.send.call_args_list]
    assert sent.count(str(dummy_posting("JobA"))) == 1
    assert sent.count(str(dummy_posting("JobB"))) == 1
