

# could use some upgrading

import datetime
import nextcord


suggestion_channel_name = "💡suggestions"
def setup(bot):
    
    @bot.slash_command(name="setup_suggestions", description="Sets up a suggestion channel")
    async def setup_suggestions(interaction: nextcord.Interaction):
        suggestion_category_name = "📝 Suggestions"
        suggestion_category = await interaction.guild.create_category(suggestion_category_name)

        overwrites = {
        interaction.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
    }
        suggestion_channel = await interaction.guild.create_text_channel(suggestion_channel_name, category=suggestion_category, overwrites=overwrites)

        await interaction.send("Suggestion channel has been set up.")


    @bot.slash_command(name="suggest", description="Submit a suggestion")
    async def suggest(interaction: nextcord.Interaction, title: str, description: str):
        suggestion_channel = nextcord.utils.get(interaction.guild.text_channels, name=suggestion_channel_name)

        if suggestion_channel is None:
            await interaction.send("Suggestion channel not found. Please set up a suggestion channel using /setup_suggestions first.", ephemeral=True)
            return

        embed = nextcord.Embed(title=f"📢 {title}", description=description, color=nextcord.Color.blue(), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Suggested by {interaction.user}", icon_url=interaction.user.avatar.url)
        
        # Send the suggestion and add reactions
        suggestion_message = await suggestion_channel.send(embed=embed)
        await suggestion_message.add_reaction("⬆️")
        await suggestion_message.add_reaction("⬇️")

        await interaction.send("Your suggestion has been received.", ephemeral=True)