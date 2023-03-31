





import io
import nextcord
from nextcord import Interaction

async def generate_server_structure(guild):
    structure = []

    structure.append(f"Server Name: {guild.name}")
    structure.append("Categories:")

    for category in guild.categories:
        structure.append(f"  - {category.name}")

    structure.append("Channels:")

    for channel in guild.channels:
        structure.append(f"  - {channel.name}")

    structure.append("Roles:")

    for role in guild.roles:
        structure.append(f"  - {role.name}")

    return "\n".join(structure)


def setup(bot):
    @bot.slash_command(name="save_template", description="Saves the current server as a template and sends it as a message to a specified channel.")
    async def save_template(interaction: Interaction):
        # Check if the user has admin privileges
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must have administrator privileges to use this command.", ephemeral=True)
            return

        name = "My Server Template"
        server_structure = await generate_server_structure(interaction.guild)

        # Create a .txt file with the server structure
        structure_file = io.BytesIO(server_structure.encode())
        file = nextcord.File(structure_file, filename=f"{name}.txt")

        await interaction.response.send_message("Sending the server template...", ephemeral=True)
        await interaction.channel.send(file=file)