

import nextcord 
import asyncio
import feedparser


def setup(bot):
    @bot.slash_command()
    async def send_news(interaction: nextcord.Interaction):
        """Send news updates to a specified channel."""
        await interaction.response.defer()
        await interaction.followup.send("Please provide the channel where the news updates should be sent:", ephemeral=True)
        response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
        channel = response.channel_mentions[0]
        
        await interaction.followup.send("Sending news updates to " + channel.mention, ephemeral=True)
        
        feed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
        index = 0

        while True:
            post = feed.entries[index]
            await channel.send(post.title + ": " + post.link)
            index = (index + 1) % len(feed.entries)
            await asyncio.sleep(300) #should be 5 mins before the next news post