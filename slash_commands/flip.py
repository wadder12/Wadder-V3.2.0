



import random
from nextcord import Interaction


def setup(bot):

    @bot.slash_command(description="Flip a coin")
    async def flip(interaction: Interaction):
        result = random.choice(["heads", "tails"])
        await interaction.response.send_message(f"The coin landed on {result}!")