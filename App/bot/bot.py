import os
import discord
import logging
from queue import Queue
from dotenv import load_dotenv

from App.models import job_posting
from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper
from App.scraper.scraper_manager import ScraperManager
from App.scraper.simplify_repo_scraper import SimplifyRepoScraper
from App.services.job_postings_sender import JobPostingsSender


CHANNEL_ID = 1395165798875533312

logger = logging.getLogger("discord")


class Bot(discord.Client):
    INTERVAL_MINUTES: int = 5
    INTERVAL_SECONDS: int = INTERVAL_MINUTES * 60

    async def on_ready(self):
        logger.info(f"Logged on as {self.user}!")

        job_postings_queue: Queue[JobPosting] = Queue()
        scrapers: list[Scraper] = [SimplifyRepoScraper()]

        scraper_manager = ScraperManager(
            scrapers=scrapers,
            interval_in_seconds=self.INTERVAL_SECONDS,
            queue=job_postings_queue,
        )

        job_postings_sender = JobPostingsSender(
            queue=job_postings_queue,
            interval_in_seconds=self.INTERVAL_SECONDS,
            channel=self.get_channel(CHANNEL_ID),
        )

        scraper_manager.run()
        job_postings_sender.run()


def start_bot():
    dotenv_loaded = load_dotenv()
    token = os.getenv("DISCORD_TOKEN")

    if not dotenv_loaded or token == None:
        raise Exception(
            "No discord application token found in .env, make sure you have a .env file with the token stored in DISCORD_TOKEN"
        )

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(intents=intents)
    bot.run(token)
