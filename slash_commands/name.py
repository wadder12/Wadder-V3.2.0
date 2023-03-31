

import nextcord


def setup(bot):
    @bot.slash_command(description="Changes the nickname of a user on the server.")
    async def nickname(interaction: nextcord.Interaction, user: nextcord.Member, nickname: str):
        """
        Changes the nickname of a user on the server.

        Args:
        - user (nextcord.Member): The member whose nickname should be changed.
        - nickname (str): The new nickname for the user.
        """
        await user.edit(nick=nickname)
        await interaction.response.send_message(f"{user.mention}'s nickname has been changed to {nickname}.")