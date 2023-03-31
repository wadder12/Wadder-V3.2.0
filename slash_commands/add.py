


import nextcord


def setup(bot):
    @bot.slash_command(description='Calculate the sum of two numbers.')
    async def add(interaction: nextcord.Interaction, num1: int, num2: int):
        """
        Calculate the sum of two numbers.

        Args:
        - num1 (int): The first number.
        - num2 (int): The second number.
        """
        # Calculate the sum of the two numbers
        result = num1 + num2

        # Send the result as a message
        await interaction.response.send_message(f'The sum of {num1} and {num2} is {result}.')