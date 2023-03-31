# update!

import nextcord


def setup(bot):
    @bot.slash_command(description='Calculate the average of a list of numbers.')
    async def calculate_average(interaction: nextcord.Interaction, numbers: str):
        """
        Calculate the average of a list of numbers.

        Args:
        - numbers (str): A comma-separated list of numbers.
        """
        # Convert the comma-separated string of numbers to a list of floats
        numbers_list = [float(n) for n in numbers.split(',')]

        # Calculate the average of the numbers
        average = sum(numbers_list) / len(numbers_list)

        # Send the calculated average as a message
        await interaction.response.send_message(f'Average: {average}')