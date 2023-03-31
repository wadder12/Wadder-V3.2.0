



import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get a random programming joke.')
    async def progjoke(interaction: nextcord.Interaction):
        """
        Get a random programming joke.
        """
        # Fetch a random programming joke from the API
        response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')

        # Extract the joke setup and punchline from the response JSON
        data = response.json()[0]
        setup = data['setup']
        punchline = data['punchline']

        # Send the joke as a message
        await interaction.response.send_message(f'{setup}\n{punchline}')