



import nextcord


def setup(bot):
    
    @bot.slash_command(description="Mute a user in a voice channel.")
    async def mutevoice(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
        """
        Mute a user in a voice channel.

        Args:
        - member (nextcord.Member): The member to mute.
        - reason (str): The reason for muting the user.
        """
        # Check if the user has permission to mute members
        if not interaction.user.guild_permissions.mute_members:
            return await interaction.response.send_message("You do not have permission to mute members.")

        await member.edit(mute=True, reason=reason)
        await interaction.response.send_message(f"{member.mention} has been muted in the voice channel. Reason: {reason}")