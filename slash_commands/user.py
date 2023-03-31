
import nextcord
from nextcord.ext import commands
from typing import Optional, List


nopings = nextcord.AllowedMentions(replied_user=False)


def split_chunks(input: str, chunks: int = 1990) -> List[str]:
    return [input[n:n + chunks] for n in range(0, len(input), chunks)]


def setup(bot):
    @bot.slash_command(name="profile", description="Displays the user's server profile picture.")
    async def profile(interaction: nextcord.Interaction, user: Optional[nextcord.Member] = None):
        """
        Correct usage: /profile <user>
        Displays the user's server profile picture
        """
        if not user:
            if not isinstance(interaction.author, nextcord.Member):
                raise Exception("Invalid caller")
            user = interaction.author
        emb: nextcord.Embed = nextcord.Embed(
            title=str(user),
            type="rich"
        )
        emb.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(
            embed=emb,
            allowed_mentions=nopings
        )