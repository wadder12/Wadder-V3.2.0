

import nextcord

def setup(bot):
    
    @bot.slash_command(description="Unban a user from the server.")
    async def unban(interaction: nextcord.Interaction, user: nextcord.User, reason: str = "No reason provided."):
        """
        Unban a user from the server.

        Args:
        - user (nextcord.User): The user to unban.
        - reason (str): The reason for the unban.
        """
        if interaction.user.guild_permissions.ban_members:
            await interaction.guild.unban(user, reason=reason)
            await interaction.response.send_message(f"{user.mention} has been unbanned. Reason: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to unban members.")