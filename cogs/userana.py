import nextcord
from nextcord.ext import commands

class UserAnalyticsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = {}
        self.channel_count = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        """Counts the number of messages sent by each user"""
        if message.author.bot:
            return
        if message.guild.id not in self.message_count:
            self.message_count[message.guild.id] = {}
        if message.author.id not in self.message_count[message.guild.id]:
            self.message_count[message.guild.id][message.author.id] = 1
        else:
            self.message_count[message.guild.id][message.author.id] += 1

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Updates the message count when a message is deleted"""
        if message.author.bot:
            return
        if message.guild.id in self.message_count and message.author.id in self.message_count[message.guild.id]:
            self.message_count[message.guild.id][message.author.id] -= 1

    @commands.command()
    async def analytics(self, ctx, user: nextcord.User = None):
        """Displays user analytics for the server"""
        guild_id = ctx.guild.id

        if user:
            message_count = self.message_count.get(guild_id, {}).get(user.id, 0)
            message_count_embed = nextcord.Embed(title=f"Message Count for {user.display_name}", description=message_count)
            await ctx.send(embed=message_count_embed)
        else:
            message_count_embed = nextcord.Embed(title="Message Count")
            for user_id, count in self.message_count.get(guild_id, {}).items():
                user = self.bot.get_user(user_id)
                if user:
                    message_count_embed.add_field(name=user.display_name, value=count)
            await ctx.send(embed=message_count_embed)

def setup(bot):
    bot.add_cog(UserAnalyticsCog(bot))