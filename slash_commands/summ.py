

import nextcord
import openai


def setup(bot):
    @bot.slash_command()
    async def summarize(interaction: nextcord.Interaction, text: str):
        """
        Summarize text using the Davinci 003 engine.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Please summarize the following text:\n{text}\nSummary:",
            max_tokens=60,
            temperature=0.7,
        )
        summary = response.choices[0].text.strip()
        await interaction.response.send_message(f"Here's a summary of the text:\n{summary}")