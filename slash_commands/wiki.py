

import nextcord
import wikipediaapi


def setup(bot):
    wiki = wikipediaapi.Wikipedia('en')
    @bot.slash_command(
    name='wikiy',
    description='Retrieve a summary of a given topic from Wikipedia.'
)
    async def wiki_summary(interaction: nextcord.Interaction, topic: str):
        """
        Retrieve a summary of a given topic from Wikipedia.

        Args:
        - topic (str): The topic to retrieve a summary for.
        """
        # Retrieve the summary for the given topic from Wikipedia
        page = wiki.page(topic)
        if page.exists():
            summary = page.summary
        else:
            summary = f'Unable to retrieve a summary for "{topic}" at this time.'

        # Split the summary into chunks of 2000 characters or less
        chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]

        # Send each chunk as a separate message
        for chunk in chunks:
            await interaction.response.send_message(chunk)