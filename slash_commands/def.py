
import nextcord

def setup(bot):
    @bot.slash_command(description="Deafen a user in a voice channel.")
    async def deafen(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
        """
        Deafen a user in a voice channel.

        Args:
        - member (nextcord.Member): The member to deafen.
        - reason (str): The reason for deafening the user.
        """
        # Check if the user has permission to deafen members
        if not interaction.user.guild_permissions.deafen_members:
            return await interaction.response.send_message("You do not have permission to deafen members in voice channels.")

        await member.edit(deafen=True, reason=reason)
        await interaction.response.send_message(f"{member.mention} has been deafened in the voice channel. Reason: {reason}")