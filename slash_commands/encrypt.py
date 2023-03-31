

import nextcord


def setup(bot):
    @bot.slash_command(description='Encrypt text using the Caesar cipher.')
    async def encrypt_caesar(
        interaction: nextcord.Interaction,
        text: str,
        shift: int
    ):
        # Convert text to uppercase
        text = text.upper()

        # Define alphabets for encryption
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]

        # Encrypt the text using the Caesar cipher
        encrypted_text = ''
        for char in text:
            if char in alphabet:
                encrypted_text += shifted_alphabet[alphabet.index(char)]
            else:
                encrypted_text += char

        # Send the encrypted text to the user
        await interaction.response.send_message(f'Encrypted text: `{encrypted_text}`')