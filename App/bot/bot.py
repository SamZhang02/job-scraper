import os
import discord
import logging
from queue import Queue
from dotenv import load_dotenv

from App.models.job_posting import JobPosting
from App.scraper.scraper import Scraper
from App.scraper.scraper_manager import ScraperManager
from App.scraper.simplify_repo_scraper import SimplifyRepoScraper
from App.scraper.job_pulse_scraper import JobPulseScraper
from App.services.job_postings_sender import JobPostingsSender


CHANNEL_ID = 1395165798875533312
TEST_CHANNEL_ID = 1395437485290426529

DATA_DIR = os.path.join('.', "data")
POSTINGS_FILE = os.path.join(DATA_DIR, "postings")

logger = logging.getLogger("discord")




class Bot(discord.Client):
    INTERVAL_MINUTES: int = 5
    INTERVAL_SECONDS: int = INTERVAL_MINUTES * 60

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Flag to prevent reinitializing threads when the bot disconnects and reconnects
        self.began_scraping: bool = False

    async def on_ready(self):
        if self.began_scraping:
            logger.info("Already scraping, skipping setup.")
            return

        logger.info(f"Logged on as {self.user}!")

        job_postings_queue: Queue[JobPosting] = Queue()
        scrapers: list[Scraper] = [SimplifyRepoScraper(), JobPulseScraper()]

        scraper_manager = ScraperManager(
            scrapers=scrapers,
            interval_in_seconds=self.INTERVAL_SECONDS,
            queue=job_postings_queue,
        )

        job_postings_sender = JobPostingsSender(
            queue=job_postings_queue,
            interval_in_seconds=self.INTERVAL_SECONDS,
            channel=self.get_channel(CHANNEL_ID),
            persist_postings_path=POSTINGS_FILE
        )

        scraper_manager.run()
        job_postings_sender.run()

        self.began_scraping = True


def start_bot():
    os.makedirs(DATA_DIR, exist_ok=True)
    logger.info(f"Will write postings to {POSTINGS_FILE}")

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
