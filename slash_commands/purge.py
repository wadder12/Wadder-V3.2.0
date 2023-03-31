
import nextcord, re
from nextcord.ext import commands

from typing import List
import nextcord


nopings = nextcord.AllowedMentions(replied_user=False)


def split_chunks(input: str, chunks: int = 1990) -> List[str]:
    return [input[n:n + chunks] for n in range(0, len(input), chunks)]


def setup(bot):
    @bot.slash_command(name="purge", description="Purges all deleted banned accounts in the server's banlist.")
    @commands.has_permissions(ban_members=True)
    async def purge(interaction: nextcord.Interaction):
        """
        Purges all deleted banned accounts in the server's banlist.
        """
        if interaction.guild is None:
            raise Exception("Guild not found")

        bans = await interaction.guild.bans().flatten()
        banlist: list[str] = []

        pattern = re.compile(r"^Deleted User [\da-f]{8}$")

        for ban in bans:
            if pattern.match(ban.user.name):
                await interaction.guild.unban(user=ban.user, reason="Unbanned Disabled Account")
                banlist.append(str(ban.user))

        if banlist:
            if len(banlist) > 68:
                banlist = banlist[:68]
                banlist.append(f"(And {len(banlist) - 68} more)")

            banlog = "Unbanned the following disabled accounts:\n```\n" + \
                "\n".join(banlist) + "```"

            await interaction.response.send_message(
                banlog,
                allowed_mentions=nopings
            )

        else:
            await interaction.response.send_message(
                "There are no acccounts to purge",
                allowed_mentions=nopings
            )