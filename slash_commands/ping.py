






from nextcord import Interaction
import nextcord


def setup(bot):

    @bot.slash_command(description="Ping command")
    async def ping(interaction: Interaction):
        # Calculate the bot's websocket latency
        latency = bot.latency * 1000  # in milliseconds

        # Define the embed
        embed = nextcord.Embed(title="Ping", color=0xFF5733)
        embed.add_field(name="Latency", value=f"{latency:.2f} ms")

        # Define the button to refresh the ping
        async def refresh_callback(interaction: nextcord.Interaction):
            await interaction.response.edit_message(embed=embed)

        refresh_button = nextcord.ui.Button(label="Refresh", style=nextcord.ButtonStyle.secondary)
        refresh_button.callback = refresh_callback

        # Send the embed with the refresh button as a response
        view = nextcord.ui.View()
        view.add_item(refresh_button)

        await interaction.response.send_message(embed=embed, view=view)