import random
import nextcord
import requests



def setup(bot):
    @bot.slash_command()
    async def space_fact(interaction: nextcord.Interaction):
        """
        Fetch a random outer space fact.
        """
        response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/")
        if response.status_code == 200:
            planets_data = response.json()["bodies"]
            random_planet = random.choice(planets_data)
            planet_name = random_planet["englishName"]
            planet_fact = f"{planet_name} has a mean radius of {random_planet['meanRadius']} km and an escape velocity of {random_planet['escape']} m/s."
        else:
            planet_fact = "Error fetching space fact, please try again later."

        embed = nextcord.Embed(title="Random Space Fact", description=planet_fact, color=0x00ff00)
        await interaction.response.send_message(embed=embed) 