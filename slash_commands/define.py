

#update it!

import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get the definition of a word from the Merriam-Webster dictionary.')
    async def define(interaction: nextcord.Interaction, word: str):
        """
        Get the definition of a word from the Merriam-Webster dictionary.

        Args:
        - word (str): The word to define.
        """
        # Fetch the definition of the word from the API
        response = requests.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=YOUR_API_KEY_HERE')

        # Extract the first definition from the response JSON
        data = response.json()
        definition = data[0]['shortdef'][0]

        # Send the definition as a message
        await interaction.response.send_message(f'The definition of {word} is: {definition}.')