import json
import nextcord
from nextcord.ext import commands
import aiofiles

class MessageArchive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def archive_messages(self, channel):
        messages = []
        async for message in channel.history(limit=100):  # Adjust the message limit if needed
            messages.append({
                "content": message.content,
                "author": str(message.author),
                "timestamp": message.created_at.isoformat()
            })

        async with aiofiles.open(f"{channel.guild.id}_{channel.id}_archive.json", "w") as archive_file:
            await archive_file.write(json.dumps(messages, indent=2))
        
        return f"{channel.guild.id}_{channel.id}_archive.json"

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def archive(self, ctx, channel: nextcord.TextChannel):
        archive_filename = await self.archive_messages(channel)
        await ctx.send(f"Archived messages from {channel.mention}.", file=nextcord.File(archive_filename))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def archive_server(self, ctx):
        for channel in ctx.guild.text_channels:
            try:
                archive_filename = await self.archive_messages(channel)
                await ctx.send(f"Archived messages from {channel.mention}.", file=nextcord.File(archive_filename))
            except Exception as e:
                print(f"Error archiving channel {channel}: {e}")

def setup(bot):
    bot.add_cog(MessageArchive(bot))