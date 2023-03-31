

import nextcord


def setup(bot):
    @bot.slash_command(description="Sets the slowmode delay for a channel.")
    async def slowmode(interaction: nextcord.Interaction, duration: int):
        """
        Sets the slowmode delay for a channel.

        Args:
        - duration (int): The duration of the slowmode delay in seconds.
        """
        await interaction.channel.edit(slowmode_delay=duration)
        await interaction.response.send_message(f"Slowmode has been set to {duration} seconds for this channel.")