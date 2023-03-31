
# def needs updating!

import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get a random Chuck Norris joke.')
    async def chucknorris(interaction: nextcord.Interaction):
        """
        Get a random Chuck Norris joke.
        """
        # Fetch a random Chuck Norris joke from the API
        response = requests.get('https://api.chucknorris.io/jokes/random')

        # Extract the joke text from the response JSON
        joke = response.json()['value']

        # Send the joke as a message
        await interaction.response.send_message(joke) 