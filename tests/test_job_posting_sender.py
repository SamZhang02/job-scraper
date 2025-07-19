import pytest
import time

from discord import Embed
from queue import Queue
from unittest.mock import MagicMock

from App.services.job_postings_sender import JobPostingsSender
from App.models.job_posting import JobPosting
from App.util.job_posting_embedder import JobPostingEmbedder


def extract_embed_data(embed: Embed):
    return {
        "title": embed.title,
        "url": embed.url,
        "fields": [(f.name, f.value) for f in embed.fields],
    }


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

    dummyPostingA = dummy_posting("JobA")
    dummyPostingB = dummy_posting("JobB")

    queue.put(dummyPostingA)
    time.sleep(4)

    queue.put(dummyPostingA)  # should be ignored
    queue.put(dummyPostingB)  # should be sent
    time.sleep(1)

    sent_embeds = [call.kwargs["embed"] for call in channel.send.call_args_list]

    expected_embeds = [
        extract_embed_data(JobPostingEmbedder.embed(dummyPostingA)),
        extract_embed_data(JobPostingEmbedder.embed(dummyPostingB)),
    ]

    actual_embeds = [extract_embed_data(embed) for embed in sent_embeds]

    assert actual_embeds == expected_embeds
