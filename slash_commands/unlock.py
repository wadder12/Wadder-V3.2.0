



import nextcord


def setup(bot):
    @bot.slash_command(description="Unlocks a previously locked channel to allow users to send messages.")
    async def unlock(interaction: nextcord.Interaction):
        """
        Unlocks a previously locked channel to allow users to send messages.
        """
        # Check if the user has permission to unlock the channel
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("You do not have permission to unlock channels.")

        # Unlock the channel
        overwrite = nextcord.PermissionOverwrite(send_messages=True)
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("This channel has been unlocked.")