

import nextcord


def setup(bot):
    @bot.slash_command(description='Reverse a message.')
    async def reverse(interaction: nextcord.Interaction, message: str):
        # Reverse the message
        reversed_message = message[::-1]

        # Send the reversed message as a code block
        await interaction.response.send_message(f'```\n{reversed_message}\n```')