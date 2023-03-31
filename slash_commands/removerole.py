

import nextcord

def setup(bot):
    
    @bot.slash_command(description="Remove a role from a user in the server.")
    async def remove_role(interaction: nextcord.Interaction, user: nextcord.Member, role: nextcord.Role, reason: str = "No reason provided."):
        """
        Remove a role from a user in the server.

        Args:
        - user (nextcord.Member): The member to remove the role from.
        - role (nextcord.Role): The role to remove.
        - reason (str): The reason for removing the role.
        """
        if interaction.user.guild_permissions.manage_roles:
            await user.remove_roles(role, reason=reason)
            await interaction.response.send_message(f"{role.mention} has been removed from {user.mention}. Reason: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to remove roles.")