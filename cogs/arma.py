import nextcord
from nextcord.ext import commands
import requests
import asyncio


class ArmaServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_url = "https://api.battlemetrics.com/servers/19734404"  # Replace with your server ID
        self.server_stats = None
        self.refresh_task = self.bot.loop.create_task(self.refresh_server_status())

    async def refresh_server_status(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.get_server_stats()
            embed = self.get_stats_embed()
            await self.send_server_status_to_channel(embed)
            await asyncio.sleep(180)  # Refresh every 3 minutes

    async def get_server_stats(self):
        response = requests.get(self.server_url)
        if response.status_code == 200:
            self.server_stats = response.json()["data"]["attributes"]
            return True
        return False

    def get_stats_embed(self):
        if self.server_stats["status"] == "online":
            embed = nextcord.Embed(title="Arma 3 SOG", color=nextcord.Color.green())
            embed.add_field(name="Status", value="Online")
            embed.add_field(name="Players online", value=f"{self.server_stats['players']}/{self.server_stats['maxPlayers']}")
            if 'details' in self.server_stats and 'port' in self.server_stats['details']:
                embed.add_field(name="Game port", value=self.server_stats['details']['port'])
            if 'details' in self.server_stats and 'country' in self.server_stats['details']:
                embed.add_field(name="Country", value=self.server_stats['details']['country'])
            if 'details' in self.server_stats and 'uptime' in self.server_stats['details']:
                embed.add_field(name="Uptime", value=f"{self.server_stats['details']['uptime']} seconds")
            if 'details' in self.server_stats and 'map' in self.server_stats['details']:
                embed.add_field(name="Map", value=self.server_stats['details']['map'])
            if 'details' in self.server_stats and 'mission' in self.server_stats['details']:
                embed.add_field(name="Mission", value=self.server_stats['details']['mission'])
            if 'details' in self.server_stats and 'mods' in self.server_stats['details']:
                if self.server_stats['details']['mods']:
                    mods = "\n".join(self.server_stats['details']['mods'])
                    embed.add_field(name="Mods", value=mods, inline=False)

            return embed
        else:
            embed = nextcord.Embed(title="Server Status", color=nextcord.Color.red())
            embed.add_field(name="Status", value="Offline")
            return embed

    async def send_server_status_to_channel(self, embed):
        channel_id = 1052894880273268758  # Replace with your channel ID
        channel = self.bot.get_channel(channel_id)
        if channel:
            # Delete the previous status message
            def is_status_message(m):
                return m.author == self.bot.user and len(m.embeds) > 0 and m.embeds[0].title == "Server Status"

            await channel.purge(limit=1, check = is_status_message)

        # Send the new status message
        await channel.send(embed=embed)

def cog_unload(self):
    self.refresh_task.cancel()


def setup(bot):
    bot.add_cog(ArmaServerCog(bot))