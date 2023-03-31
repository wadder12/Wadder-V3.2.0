import nextcord

def setup(bot):
    # Unmute a user in the server
    @bot.slash_command(description="Unmute a user in the server.")
    async def unmute(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        """
        Unmute a user in the server.

        Args:
        - user (nextcord.Member): The member to unmute.
        - reason (str): The reason for the unmute.
        """
        role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await user.remove_roles(role, reason=reason)
        await interaction.response.send_message(f"{user.mention} has been unmuted. Reason: {reason}")