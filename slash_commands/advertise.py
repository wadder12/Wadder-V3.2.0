

import nextcord


def setup(bot):
    @bot.slash_command(
    name='advertise',
    description='Advertise the bot and its features.'
)
    async def advertise_bot(interaction: nextcord.Interaction):
        """
        Advertise the bot and its features.
        """
        # Create a message with information about the bot and its features
        message = """
        **Welcome to Wadder!**
        
        Wadder is a powerful and easy-to-use bot that can help you with a wide range of tasks. Here are some of its key features:
        
        - Slash commands for easy access to bot functionality
        - Customizable settings and preferences
        - Integration with third-party APIs for additional functionality
        - Moderation tools to help keep your server safe and secure
        - And much more!
        
        To get started with Wadder, simply invite it to your server and type `/help` to see a list of available commands.
        """

        # Send the advertisement message as a message
        await interaction.response.send_message(message)    