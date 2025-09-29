## Job Scraper Discord Bot

A simple Discord bot that polls new grad job posting repositories and send them to a Discord text channel

<p align="center">
<img width="500" height="1688" alt="CleanShot 2025-07-19 at 12 21 16@2x" src="https://github.com/user-attachments/assets/c1357e50-7fcd-4334-9859-6b785422ccfe" />
</p>

It currently only scrapes the Simplify 2026 new grad tech positions repository, more sources may be added 

## Self-Hosting
The entrypoint is locatd at `main.py`. To self-host:

0. Have a `DISCORD_TOKEN` in your `.env`
1. Install dependencies from `pyproject.toml` 
2. Change my hardcoded channel ID and polling interval in `App/bot/bot.py`
3. Run `main.py`, optionally:

```
just host
```

Runs the application in a docker container 
