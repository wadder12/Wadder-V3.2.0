

import nextcord


def setup(bot):
    @bot.slash_command(description="Adds or removes a role from a user.")
    async def role(interaction: nextcord.Interaction, user: nextcord.Member, action: str, role: nextcord.Role):
        """
        Adds or removes a role from a user.

        Args:
        - user (nextcord.Member): The member whose roles should be modified.
        - action (str): The action to perform - either "add" or "remove".
        - role (nextcord.Role): The role to add or remove.
        """
        if action.lower() == "add":
            await user.add_roles(role)
            await interaction.response.send_message(f"{user.mention} has been given the {role.name} role.")
        elif action.lower() == "remove":
            await user.remove_roles(role)
            await interaction.response.send_message(f"{user.mention} has had the {role.name} role removed.")
        else:
            await interaction.response.send_message("Invalid action. Please specify either 'add' or 'remove'.")