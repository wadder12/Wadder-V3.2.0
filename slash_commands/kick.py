


import nextcord

def setup(bot):
    
    @bot.slash_command(description="Kick a user from the server.")
    async def kick(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        """
        Kick a user from the server.

        Args:
        - user (nextcord.Member): The member to kick.
        - reason (str): The reason for the kick.
        """
        if interaction.user.guild_permissions.kick_members:
            await user.kick(reason=reason)
            await interaction.response.send_message(f"{user.mention} has been kicked. Reason: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to kick members.")