
import asyncio
from dateutil.parser import parse as parse_duration
import nextcord


def setup(bot):
    @bot.slash_command(description="Temporarily mutes a user in the server for a specified duration.")
    async def tempmute(interaction: nextcord.Interaction, user: nextcord.Member, duration: str, reason: str = "No reason provided."):
        """
        Temporarily mutes a user in the server for a specified duration.

        Args:
        - user (nextcord.Member): The member to mute.
        - duration (str): The duration of the mute (e.g. '1h', '2d').
        - reason (str): The reason for the mute.
        """
        duration_seconds = parse_duration(duration)
        await user.edit(mute=True, reason=reason)
        await interaction.response.send_message(f"{user.mention} has been muted for {duration}. Reason: {reason}")
        await asyncio.sleep(duration_seconds)
        await user.edit(mute=False, reason="Mute duration has expired.")
        await interaction.followup.send(f"{user.mention}'s mute duration has expired.")    