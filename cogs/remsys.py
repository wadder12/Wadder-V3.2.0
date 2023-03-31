import nextcord
from nextcord.ext import commands
import asyncio
import pytz

class ReminderCog(commands.Cog):
    """A customizable reminder system for Discord"""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    @commands.command()
    async def remind(self, ctx, message: str, time: str):
        """Set a reminder for a specific time"""
        user = ctx.author
        try:
            timezone = pytz.timezone(str(user.timezone))
        except AttributeError:
            await ctx.send("Please set your timezone using the `!settimezone` command before setting a reminder.")
            return
        try:
            duration = int(time)
            if duration <= 0:
                raise ValueError
        except ValueError:
            await ctx.send("Invalid duration. Please enter a positive integer number of minutes for the reminder time.")
            return
        reminder_time = timezone.localize(nextcord.utils.utcnow() + nextcord.utils.timedelta(minutes=duration))
        self.reminders[user.id] = (message, reminder_time, ctx.channel.id)
        await ctx.send(f"Reminder set for {reminder_time.strftime('%m/%d/%Y %I:%M %p')}.")

        await asyncio.sleep(duration * 60)
        if user.id in self.reminders:
            del self.reminders[user.id]
            channel = self.bot.get_channel(ctx.channel.id)
            await channel.send(f"{user.mention}, {message}")

    @commands.command()
    async def viewreminders(self, ctx):
        """View all active reminders for the user"""
        user = ctx.author
        if user.id in self.reminders:
            reminder = self.reminders[user.id]
            message = reminder[0]
            reminder_time = reminder[1].strftime('%m/%d/%Y %I:%M %p')
            channel = self.bot.get_channel(reminder[2])
            await ctx.send(f"Reminder: `{message}` at {reminder_time} in {channel.mention}")
        else:
            await ctx.send("You have no active reminders.")

    @commands.command()
    async def deletereminder(self, ctx):
        """Delete an active reminder"""
        user = ctx.author
        if user.id in self.reminders:
            del self.reminders[user.id]
            await ctx.send("Reminder deleted.")
        else:
            await ctx.send("You have no active reminders to delete.")

    @commands.command()
    async def settimezone(self, ctx, timezone: str):
        """Set the user's timezone for reminder scheduling"""
        user = ctx.author
        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            await ctx.send("Invalid timezone. Please enter a valid timezone in the format 'Area/Location' (e.g., 'US/Eastern').")
            return
        user.timezone = timezone
        await ctx.send(f"Timezone set to {timezone}.")
        
        
def setup(bot):
    bot.add_cog(ReminderCog(bot))