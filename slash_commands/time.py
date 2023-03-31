# good but make a embed for it! & make it in non-miltary time!


import datetime
import nextcord
from nextcord import Interaction


def setup(bot):
    @bot.slash_command(name='get_the_time', description='Get you the time!')
    async def time(interaction: Interaction):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        await interaction.response.send_message(f"The current time is {current_time}")