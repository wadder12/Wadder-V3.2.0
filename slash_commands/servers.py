





import nextcord

def setup(bot):
    @bot.slash_command(name='get_servers', description="Displays the list of servers Wadder bot is in.")
    async def serverswbot(interaction: nextcord.Interaction):
        servers = interaction.client.guilds
        message = f"**Wadder Bot Server List**\n\nMy bot is currently in {len(servers)} servers. Here is a list of them:\n\n"

        for server in servers:
            server_link = f"https://discord.com/channels/{server.id}"
            server_name = server.name
            member_count = server.member_count
            message += f"- [{server_name}]({server_link}) ({member_count} members)\n"

        await interaction.response.send_message(message)