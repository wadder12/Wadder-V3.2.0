


import nextcord
from nextcord import Interaction
import openai


def setup(bot):

    @bot.slash_command(name="chatbot", description="Chat with an AI bot")
    async def chatbot(interaction:Interaction):
        await interaction.response.defer()

        # Set up the OpenAI API
        openai.api_key = "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"

        # Begin the chat loop
        while True:
            # Prompt the user for a question or message for the chatbot
            await interaction.followup.send("What would you like to ask the chatbot? (Enter 'quit' to exit)")

            # Wait for the user to enter their question or message
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content != ""

            user_input = await bot.wait_for('message', check=check)

            # Check if the user wants to quit
            if user_input.content.lower() == "quit":
                break

            # Generate a response using OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",  # The model to use
                prompt=user_input.content,  # The user's question or message
                temperature=0.5,  # How "creative" the response should be
                max_tokens=512,  # The maximum number of tokens (words) in the response
                n=1,  # The number of responses to generate
                stop=None,  # Stop generating responses when one of these strings is encountered
            )

            # Send the response to the user in Discord
            response_text = response.choices[0].text
            print(f"Sending response to channel {interaction.channel}: {response_text}")
            await interaction.followup.send(response_text)

        # Send a goodbye message when the user is done
        await interaction.followup.send("Goodbye!")