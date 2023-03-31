# needs updating in v3.1



import nextcord


def setup(bot):
    @bot.slash_command(description="Send a customized announcement.")
    async def announce(
        interaction: nextcord.Interaction,
        title: str,
        message: str,
        channel: nextcord.TextChannel,
        mention: bool = False
    ):
        """
        Send a customized announcement in the specified channel.

        Args:
        - title (str): The title of the announcement.
        - message (str): The message to be included in the announcement.
        - channel (nextcord.TextChannel): The channel to send the announcement in.
        - mention (bool): Whether or not to mention the @everyone role in the announcement. Defaults to False.
        """
        # Create the announcement embed
        embed = nextcord.Embed(
            title=title,
            description=message,
            color=0xff0000
        )
        
        # Mention @everyone if requested
        if mention:
            content = "@everyone"
        else:
            content = None
        
        # Send the announcement message
        await channel.send(content=content, embed=embed)
        
        # Send a response to the user
        await interaction.response.send_message(f"Announcement sent in {channel.mention}!")