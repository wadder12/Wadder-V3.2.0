import nextcord
from nextcord.ext import commands
bot = commands.Bot(command_prefix='/', intents=nextcord.Intents.all())



def setup(bot):
    @bot.command()
    async def hellotest(ctx):
        await ctx.send("Hello!")