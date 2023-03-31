


from datetime import timedelta
import datetime
import nextcord


def setup(bot):
    @bot.slash_command()
    async def poll(interaction: nextcord.Interaction, time: int, title: str, options: str):
        """
        Example: /poll 30 "Favorite Color" "Red|Green|Blue"
        """

        # Check if required parameters are missing
        if not all((time, title, options)):
            await interaction.response.send_message("Please specify the time, title, and options!", ephemeral=True)
            return

        # Parse options from input string
        options = options.split('|')

        # Check if too many options were provided
        MAX_OPTIONS = 6
        if len(options) > MAX_OPTIONS:
            await interaction.response.send_message(f"Maximum number of options is {MAX_OPTIONS}!", ephemeral=True)
            return

        # Calculate poll end time
        end_time = datetime.now() + timedelta(minutes=time)
        formatted_end_time = nextcord.utils.format_dt(end_time, style="T")

        # Create and send embed with poll options
        options_text = "\n".join([f"`{i}.` {option}" for i, option in enumerate(options, start=1)])

        # Define the color for the embed
        EMBED_COLOR = 0x3498db

        embed = nextcord.Embed(color=EMBED_COLOR, title=title)
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.set_footer(text=f"Poll ends at {formatted_end_time}")

        poll_message = await interaction.channel.send(embed=embed)

        # Add reactions to poll message
        for i in range(1, len(options) + 1):
            await poll_message.add_reaction(f"{i}\uFE0F\u20E3")

        # Send confirmation message to user
        await interaction.response.send_message(f"Poll created in {interaction.channel.mention}!", ephemeral=True)