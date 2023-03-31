

# update needed

import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get a random dad joke.')
    async def dadjoke(interaction: nextcord.Interaction):
        """
        Get a random dad joke.
        """
        # Fetch a random dad joke from the API
        response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'})

        # Extract the joke text from the response
        joke = response.text

        # Send the joke as a message
        await interaction.response.send_message(joke)
