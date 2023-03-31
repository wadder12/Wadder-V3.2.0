
import nextcord

def setup(bot):
    
    @bot.slash_command(description="Add a role to a user in the server.")
    async def add_role(interaction: nextcord.Interaction, user: nextcord.Member, role: nextcord.Role, reason: str = "No reason provided."):
        """
        Add a role to a user in the server.

        Args:
        - user (nextcord.Member): The member to add the role to.
        - role (nextcord.Role): The role to add.
        - reason (str): The reason for adding the role.
        """
        if interaction.user.guild_permissions.manage_roles:
            await user.add_roles(role, reason=reason)
            await interaction.response.send_message(f"{role.mention} has been added to {user.mention}. Reason: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to add roles.")