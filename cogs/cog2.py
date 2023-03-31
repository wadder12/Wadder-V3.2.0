import nextcord
from nextcord.ext import commands

class Cog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello1(self, ctx):
        await ctx.send("Hello from Cog1!")

def setup(bot):
    bot.add_cog(Cog1(bot))