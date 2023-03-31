import nextcord

def setup(bot):
    @bot.slash_command(description="Undeafen a user in a voice channel.")
    async def undeafen(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
        """
        Undeafen a user in a voice channel.

        Args:
        - member (nextcord.Member): The member to undeafen.
        - reason (str): The reason for undeafening the user.
        """
        # Check if the user has permission to deafen members
        if not interaction.user.guild_permissions.deafen_members:
            return await interaction.response.send_message("You do not have permission to deafen members in voice channels.")

        await member.edit(deafen=False, reason=reason)
        await interaction.response.send_message(f"{member.mention} has been undeafened in the voice channel. Reason: {reason}")