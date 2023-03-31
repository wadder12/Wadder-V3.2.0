# needs updating fast

import asyncio
import nextcord
import requests


def setup(bot):
    @bot.slash_command(
    name="game_deals",
    description="Sends a notification with details about any free or discounted games on Steam."
)
    async def send_game_deals(ctx, channel: nextcord.TextChannel):
        """
        Sends a notification to the specified channel with details about any free or discounted games on Steam.
        """
        while True:
            # Make a GET request to the Steam API to get a list of current specials
            url = "https://store.steampowered.com/api/featuredcategories"
            params = {
                "cc": "US",
                "l": "en",
                "v": 1,
                "tag": "specials"
            }
            response = requests.get(url, params=params)

            # Parse the JSON response to get a list of games on sale or for free
            data = response.json()
            specials = data["specials"]["items"]

            # Create an embed to send to the notification channel
            embed = nextcord.Embed(title="New game deals available on Steam:", color=0x00ff00)
            for game in specials:
                if game["discount_percent"] > 0:
                    discount_price = game.get("discount_final_price_formatted")
                    embed.add_field(name=f"{game['name']} - {game['discount_percent']}% off",
                                    value=f"{discount_price}", inline=False)
                else:
                    embed.add_field(name=f"{game['name']} - free to play!", value="\u200b", inline=False)

            # Send the embed to the specified notification channel and delete the previous message if it exists
            if hasattr(send_game_deals, "last_message"):
                await send_game_deals.last_message.delete()
            send_game_deals.last_message = await channel.send(embed=embed)

            # Send a confirmation message to the command author
            await ctx.send(f"Game deals notification sent to {channel.mention}!")

            # Wait for 24 hours before checking for updates again
            await asyncio.sleep(24 * 60 * 60)