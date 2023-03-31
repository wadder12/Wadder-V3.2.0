
# could use someupdating 
import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get the lyrics of a song.')
    async def lyrics(interaction: nextcord.Interaction, artist: str, song: str):
        """
        Get the lyrics of a song.

        Args:
        - artist (str): The artist of the song.
        - song (str): The title of the song.
        """
        # Fetch the lyrics of the song from the API
        response = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{song}')

        # Extract the lyrics from the response JSON
        data = response.json()
        lyrics = data['lyrics']

        # Send the lyrics as a message
        await interaction.response.send_message(lyrics)