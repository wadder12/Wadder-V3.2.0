import asyncio
import nextcord
from nextcord.ext import commands
import json

def update_guilds_file(guilds):
    with open("guilds.json", "w") as f:
        json.dump(guilds, f)

def load_guilds_file():
    try:
        with open("guilds.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
COUNTERS = {
    'members': lambda guild: len(guild.members),
    'bots': lambda guild: len([member for member in guild.members if member.bot]),
    'online': lambda guild: len([member for member in guild.members if member.status == nextcord.Status.online]),
    'voice_channels': lambda guild: len(guild.voice_channels),
    'text_channels': lambda guild: len(guild.text_channels),
    'roles': lambda guild: len(guild.roles),
    'emojis': lambda guild: len(guild.emojis),
}

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_interval = 60
        self.enabled_guilds = load_guilds_file()
    async def update_counters(self, guild):
        for channel in guild.channels:
            if channel.name.startswith('Stats-'):
                counter_name = channel.name.split('-')[-1]
                counter_func = COUNTERS.get(counter_name)

                if counter_func:
                    new_name = f'Stats-{counter_name}: {counter_func(guild)}'
                    await channel.edit(name=new_name)

    async def create_counter_channel(self, guild, category, counter_name, counter_func):
        if len(category.channels) >= 5:
            return  # Reached maximum number of channels

        counter_channel_name = f'🔢 Stats-{counter_name}: {counter_func(guild)}'
        overwrites = {guild.default_role: nextcord.PermissionOverwrite(send_messages=False)}
        await guild.create_text_channel(counter_channel_name, overwrites=overwrites, category=category)

    async def create_or_update_counters(self, guild, selected_counters=None):
        if selected_counters is None:
            selected_counters = COUNTERS.keys()

        category_name = "📊 ServerStats"
        category = nextcord.utils.get(guild.categories, name=category_name)

        if not category:
            category = await guild.create_category(category_name)

        for counter_name in selected_counters:
            counter_func = COUNTERS.get(counter_name)
            if counter_func:
                counter_channel_name = f'🔢 Stats-{counter_name}: {counter_func(guild)}'
                counter_channel = nextcord.utils.get(guild.channels, name=counter_channel_name, category=category)

                if not counter_channel:
                    await self.create_counter_channel(guild, category, counter_name, counter_func)
                else:
                    await self.update_counters(guild)

    async def update_server_stats(self):
        while True:
            for guild_id in self.enabled_guilds:
                guild = self.bot.get_guild(int(guild_id))
                if guild:
                    await self.create_or_update_counters(guild)
            await asyncio.sleep(self.update_interval)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enable_server_stats(self, ctx):
        guild = ctx.guild
        if str(guild.id) not in self.enabled_guilds:
            self.enabled_guilds[str(guild.id)] = True
            update_guilds_file(self.enabled_guilds)
            await ctx.send("ServerStats enabled for this server.")
        else:
            await ctx.send("ServerStats is already enabled for this server.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable_server_stats(self, ctx):
        guild = ctx.guild
        if str(guild.id) in self.enabled_guilds:
            del self.enabled_guilds[str(guild.id)]
            update_guilds_file(self.enabled_guilds)
            await ctx.send("ServerStats disabled for this server.")
        else:
            await ctx.send("ServerStats is not enabled for this server.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if str(guild.id) in self.enabled_guilds:
            await self.create_or_update_counters(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if str(guild.id) in self.enabled_guilds:
            del self.enabled_guilds[str(guild.id)]
            update_guilds_file(self.enabled_guilds)

def setup(bot):
    bot.add_cog(ServerStats(bot))