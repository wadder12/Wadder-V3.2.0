

import asyncio
import nextcord


def setup(bot):
    @bot.slash_command(description="Temporarily bans a user from the server for a specified duration.")
    async def tempban(interaction: nextcord.Interaction, user: nextcord.Member, duration: int, reason: str = "No reason provided."):
        """
        Temporarily bans a user from the server for a specified duration.

        Args:
        - user (nextcord.Member): The member to temporarily ban.
        - duration (int): The duration of the ban in seconds.
        - reason (str): The reason for the ban.
        """
        await user.ban(reason=reason, delete_message_days=0)
        await interaction.response.send_message(f"{user.mention} has been temporarily banned for {duration} seconds. Reason: {reason}")
        await asyncio.sleep(duration)
        await user.unban()    