

import asyncio
import datetime
import nextcord
from dateutil import parser

def setup(bot):
    @bot.slash_command()
    async def countdown(interaction: nextcord.Interaction, event_name: str):
        """Countdown to a specified event."""
        await interaction.response.defer()

        await interaction.followup.send(f"What's the date and time of the {event_name}? (Please use the following format: YYYY-MM-DD HH:MM)", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        try:
            event_datetime = await bot.wait_for('message', check=check, timeout=30.0)
            event_datetime = event_datetime.content.strip()
            event_datetime = parser.parse(event_datetime)
        except nextcord.NotFound:
            await interaction.followup.send("Sorry, I couldn't find your response. Please try again.", ephemeral=True)
            return
        except asyncio.TimeoutError:
            await interaction.followup.send("Sorry, you didn't respond in time. Please try again.", ephemeral=True)
            return
        except ValueError:
            await interaction.followup.send("Sorry, that's not a valid date and time. Please try again.", ephemeral=True)
            return

        now = datetime.utcnow()
        time_diff = event_datetime - now

        days, seconds = time_diff.days, time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        countdown = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until {event_name}!"

        await interaction.followup.send(countdown, ephemeral=True)