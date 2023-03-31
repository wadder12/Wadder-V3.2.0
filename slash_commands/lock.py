

import nextcord 


def setup(bot):
    @bot.slash_command(description="Locks a channel to prevent users from sending messages.")
    async def lock(interaction: nextcord.Interaction):
        """
        Locks a channel to prevent users from sending messages.
        """
        # Check if the user has permission to lock the channel
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("You do not have permission to lock channels.")

        # Lock the channel
        overwrite = nextcord.PermissionOverwrite(send_messages=False)
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("This channel has been locked.")