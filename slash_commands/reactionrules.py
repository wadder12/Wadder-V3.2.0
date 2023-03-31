
import nextcord
import json


reaction_role_channel_name = "🎭reaction-roles"
async def save_reaction_roles(guild_id, reaction_roles):
    with open(f"{guild_id}_reaction_roles.json", "w") as file:
        json.dump(reaction_roles, file, indent=4)

async def load_reaction_roles(guild_id):
    try:
        with open(f"{guild_id}_reaction_roles.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def setup(bot):
    

    @bot.slash_command(name="setup_reaction_roles", description="Sets up a reaction role channel")
    async def setup_reaction_roles(interaction: nextcord.Interaction):
        reaction_role_category_name = "🔧 Server Utilities"
        reaction_role_category = await interaction.guild.create_category(reaction_role_category_name)

        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
        }
        reaction_role_channel = await interaction.guild.create_text_channel(reaction_role_channel_name, category=reaction_role_category, overwrites=overwrites)

        await interaction.send("Reaction role channel has been set up.")

    @bot.slash_command(name="add_reaction_role", description="Add a reaction role")
    async def add_reaction_role(interaction: nextcord.Interaction, role: nextcord.Role, emoji: str, title: str, description: str):
        reaction_role_channel = nextcord.utils.get(interaction.guild.text_channels, name=reaction_role_channel_name)

        if reaction_role_channel is None:
            await interaction.send("Reaction role channel not found. Please set up a reaction role channel using /setup_reaction_roles first.", ephemeral=True)
            return

        embed = nextcord.Embed(title=f"{emoji} {title}", description=description, color=role.color)
        embed.set_footer(text=f"React with {emoji} to get the {role.name} role")
        
        # Send the reaction role message and add the specified reaction
        reaction_role_message = await reaction_role_channel.send(embed=embed)
        await reaction_role_message.add_reaction(emoji)

        # Save the reaction role configuration
        guild_id = str(interaction.guild.id)
        reaction_roles = await load_reaction_roles(guild_id)
        reaction_roles[str(reaction_role_message.id)] = {"emoji": emoji, "role_id": role.id}
        await save_reaction_roles(guild_id, reaction_roles)

        await interaction.send("Reaction role has been added.", ephemeral=True)

    async def on_raw_reaction_add(payload):
        if payload.member.bot:
            return

        guild_id = str(payload.guild_id)
        reaction_roles = await load_reaction_roles(guild_id)
        role_info = reaction_roles.get(str(payload.message_id))

        if role_info and role_info["emoji"] == str(payload.emoji):
            role = payload.member.guild.get_role(role_info["role_id"])
            if role:
                await payload.member.add_roles(role)

    bot.add_listener(on_raw_reaction_add, 'on_raw_reaction_add')