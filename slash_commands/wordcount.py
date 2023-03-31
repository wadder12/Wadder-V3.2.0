# should be able to upgrade this! v3.1

import nextcord

def setup(bot):
    @bot.slash_command(description='Count the number of words in a message.')
    async def word_count(interaction: nextcord.Interaction, message: str):
        # Count the number of words in the message
        word_count = len(message.split())

        # Send the word count as a code block
        await interaction.response.send_message(f'```\n{word_count}\n```')