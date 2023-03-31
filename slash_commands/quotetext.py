

import nextcord


def setup(bot):
    @bot.slash_command(description='Format text as a quote.')
    async def quotetext(interaction: nextcord.Interaction, text: str):
        """
        Format text as a quote.

        Args:
        - text (str): The text to format as a quote.
        """
        # Create the quote block
        quote_block = f'```\n{text}\n```'

        # Send the quote block as a message
        await interaction.response.send_message(quote_block)
        
        