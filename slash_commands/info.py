





import nextcord
from nextcord import Interaction


def setup(bot):
    @bot.slash_command(name="server_info", description="Display Information about the Server")
    async def serverinfo(interaction: Interaction):
        guild = interaction.guild
        embed = nextcord.Embed(title=f"Server Info: {guild.name}", color=0x00ff00)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Server Region", value=str(guild.region).capitalize(), inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Text Channels", value=f"{len(guild.text_channels):,}")
        embed.add_field(name="Voice Channels", value=f"{len(guild.voice_channels):,}")
        embed.add_field(name="Roles", value=f"{len(guild.roles):,}")
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text=f"Requested by {interaction.user}")
        embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)    