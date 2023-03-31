

import nextcord


def setup(bot):
    @bot.slash_command(description='Return the input text as a code block.')
    async def codeblock(interaction: nextcord.Interaction, text: str):
        codeblock_text = f'```{text}```'
        await interaction.response.send_message(codeblock_text)