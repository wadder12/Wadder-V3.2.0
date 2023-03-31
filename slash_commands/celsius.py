

import nextcord


def setup(bot):
    @bot.slash_command(
    name='celsius',
    description='Convert a temperature from Celsius to Fahrenheit.'
)
    async def celsius_to_fahrenheit(interaction: nextcord.Interaction, celsius: float):
        """
        Convert a temperature from Celsius to Fahrenheit.

        Args:
        - celsius (float): The temperature in Celsius to convert.
        """
        # Convert the temperature from Celsius to Fahrenheit
        fahrenheit = (celsius * 9/5) + 32

        # Send the converted temperature as a message
        message = f'{celsius} degrees Celsius is equal to {fahrenheit} degrees Fahrenheit.'
        await interaction.response.send_message(message)    