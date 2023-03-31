# works, want a embed and maybe an update?

import random
from nextcord import Interaction


def setup(bot):
    @bot.slash_command(description="Roll some dice")
    async def roll(interaction: Interaction, num_dice: int):
        if num_dice < 1:
            await interaction.response.send_message("Please specify a positive number of dice to roll.")
            return
        dice = [random.randint(1, 6) for _ in range(num_dice)]
        response = f"Rolling {num_dice} dice: {', '.join(str(die) for die in dice)}"
        await interaction.response.send_message(response)   