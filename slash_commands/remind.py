
# upgrade this!

import asyncio
import nextcord


def setup(bot):
    @bot.slash_command(description="Set a reminder message to repeat in a set amount of hours.")
    async def remind(
        interaction: nextcord.Interaction,
        title: str,
        message: str,
        channel: nextcord.TextChannel,
        repeat_hours: int,
        mention: bool = False
    ):
        """
        Set a reminder message to repeat in a set amount of hours.

        Args:
        - title (str): The title of the reminder message.
        - message (str): The message to be included in the reminder.
        - channel (nextcord.TextChannel): The channel to send the reminder in.
        - repeat_hours (int): The number of hours to wait before repeating the reminder message.
        - mention (bool): Whether or not to mention the @everyone role in the reminder message. Defaults to False.
        """
        # Check if the user has permission to set reminders
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You do not have permission to set reminders.")

        # Create the reminder embed
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
        
        # Send the initial reminder message
        reminder_msg = await channel.send(content=content, embed=embed)
        
        # Send a response to the user
        await interaction.response.send_message(f"Reminder set for {repeat_hours} hours in {channel.mention}!")
        
        # Define a function to repeat the reminder message
        async def repeat_reminder():
            await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours
            while True:
                # Send the reminder message
                reminder_msg = await channel.send(content=content, embed=embed)
                await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours again
        
        # Start the repeating reminder loop as a background task
        bot.loop.create_task(repeat_reminder())