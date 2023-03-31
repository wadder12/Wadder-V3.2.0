


import base64

import nextcord


def setup(bot):
    @bot.slash_command(description='Encode a message in Base64.')
    async def encodebase64(interaction: nextcord.Interaction, message: str):
        # Encode the message in Base64
        encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')

        # Send the encoded message as a code block
        await interaction.response.send_message(f'```\n{encoded_message}\n```')