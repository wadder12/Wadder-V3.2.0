

import nextcord


def setup(bot):
    # Mute a user in the server
    @bot.slash_command(description="Mute a user in the server.")
    async def mute(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        """
        Mute a user in the server.

        Args:
        - user (nextcord.Member): The member to mute.
        - reason (str): The reason for the mute.
        """
        role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await user.add_roles(role, reason=reason)
        await interaction.response.send_message(f"{user.mention} has been muted. Reason: {reason}")
