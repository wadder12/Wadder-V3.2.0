

import nextcord

def setup(bot):
    
    @bot.slash_command(description="Ban a user from the server.")
    async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        """
        Ban a user from the server.

        Args:
        - user (nextcord.Member): The member to ban.
        - reason (str): The reason for the ban.
        """
        if interaction.user.guild_permissions.ban_members:
            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user.mention} has been banned. Reason: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to ban members.")