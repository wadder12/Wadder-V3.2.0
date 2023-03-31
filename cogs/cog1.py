import nextcord
from nextcord.ext import commands

class Cog2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello2(self, ctx):
        await ctx.send("Hello from Cog2!")

def setup(bot):
    bot.add_cog(Cog2(bot))