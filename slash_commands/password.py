


import random
import string
import nextcord


def setup(bot):
    @bot.slash_command(description='Generate a random password.')
    async def generatepassword(interaction: nextcord.Interaction, length: int = 16):
        # Generate a random password of the specified length
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Send the password as a code block
        await interaction.response.send_message(f'```\n{password}\n```')   
    