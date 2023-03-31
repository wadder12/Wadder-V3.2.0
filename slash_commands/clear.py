"""
not sure if this works or not (i am to fast) and want to upgrade this!
"""



import nextcord


def setup(bot):

    @bot.slash_command(description="Deletes a specified number of messages from a channel.")
    async def clear(interaction: nextcord.Interaction, number: int):
        """
        Deletes a specified number of messages from a channel.

        Args:
            - number (int): The number of messages to delete.
        """
        # Check if the user has permission to clear messages
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("You do not have permission to clear messages.")

        # Delete the messages
        deleted = await interaction.channel.purge(limit=number + 1)

        # Send a message indicating the number of messages deleted
        message = f"{len(deleted) - 1} messages have been deleted."
        await interaction.response.send_message(message)