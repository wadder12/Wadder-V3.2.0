

import nextcord


def setup(bot):
    @bot.slash_command(name="startlanguage", description="Start learning a new language.")
    async def start_learning(interaction: nextcord.Interaction):
        await interaction.response.send_message("Welcome to the Language Learning Bot! 🌍\n\nLet's start by choosing a language to learn:\n- Spanish\n- French\n- German\n...")