
# could use some updating!

import random
import nextcord
import requests


def setup(bot):
    @bot.slash_command(description='Get a random trivia question.')
    async def trivia(interaction: nextcord.Interaction):
        """
        Get a random trivia question.
        """
        # Fetch a random trivia question from the API
        response = requests.get('https://opentdb.com/api.php?amount=1')

        # Extract the question and answer choices from the response JSON
        data = response.json()['results'][0]
        question = data['question']
        choices = data['incorrect_answers'] + [data['correct_answer']]
        random.shuffle(choices)

        # Format the answer choices as a string
        choices_str = '\n'.join(choices)

        # Send the question and answer choices as a message
        await interaction.response.send_message(f'{question}\n\n{choices_str}')