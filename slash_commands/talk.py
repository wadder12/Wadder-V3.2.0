

# could use some updating!


import nextcord


def setup(bot):
    
    @bot.slash_command(description="Make the bot talk in a channel.")
    async def talk(
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel,
        message: str
    ):
        """
        Make the bot talk in a channel.

        Args:
        - channel (nextcord.TextChannel): The channel to send the message in.
        - message (str): The message to be sent in the channel.
        """
        # Check if the user has permission to send messages in the specified channel
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("You do not have permission to send messages in the specified channel.")
        
        # Send the message to the specified channel
        await channel.send(message)

        # Send a response to the user
        await interaction.response.send_message(f"Message sent to {channel.mention}!")