# good, but lets make it go to another channel!


import nextcord
from nextcord.ext import commands
import asyncio
from time import time



scheduled_events = dict()

async def execute_scheduled_event(event_key):
    event = scheduled_events[event_key]
    t, function, args, kwargs = event
    await asyncio.sleep(t - time())

    try:
        await function(*args, **kwargs)
    except Exception as e:
        import traceback
        print("[EXCEPTION IN SCHEDULED EVENT]")
        print(e)
        print(traceback.format_exc())

    del scheduled_events[event_key]
def setup(bot):
    
    @bot.slash_command(name="schedule", description="Schedules a message to be sent after the specified delay (in seconds).")
    async def schedule(interaction: nextcord.Interaction, delay: int, message: str):
        await interaction.response.send_message(f"Scheduling your message in {delay} seconds.")
        event_key = object()
        t = time() + delay
        function = interaction.channel.send
        args = (message,)

        scheduled_events[event_key] = (t, function, args, {})
        asyncio.create_task(execute_scheduled_event(event_key))
