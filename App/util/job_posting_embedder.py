from discord import Embed

from App.models.job_posting import JobPosting


class JobPostingEmbedder:

    @staticmethod
    def embed(posting: JobPosting) -> Embed:
        return (
            Embed(
                title=posting.title,
                url=posting.url,
            )
            .add_field(name="Company", value=posting.company, inline=False)
            .add_field(name="Locations", value=posting.locations, inline=False)
            .add_field(name="Source", value=posting.source, inline=False)
        )
