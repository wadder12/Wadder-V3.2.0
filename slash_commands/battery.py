import nextcord
from nextcord.ext import commands
import subprocess
import json


from typing import List



nopings = nextcord.AllowedMentions(replied_user=False)


def split_chunks(input: str, chunks: int = 1990) -> List[str]:
    return [input[n:n + chunks] for n in range(0, len(input), chunks)]

def setup(bot):
    @bot.slash_command(name="battery", description="Displays the status of the battery of the bot's host system.")
    async def battery(interaction: nextcord.Interaction):
        """
        Displays the status of the battery of the bot's host system
        """
        async with interaction.channel.typing():
            out = subprocess.check_output(
                args="termux-battery-status",
                shell=True
            )
        data: dict = json.loads(out.decode("utf-8"))
        perc: int = data["percentage"]

        emoji: str = ""
        match(data["status"]):
            case "CHARGING":
                emoji = "⚡"
            case "FULL":
                emoji = "🔌"
            case "DISCHARGING":
                emoji = "🪫" if perc < 30 else "🔋"

        emb: nextcord.Embed = nextcord.Embed(
            type="rich",
            colour=0xFF0000 if perc < 30 else 0x0000FF,
            title="Battery percentage:",
            description=f"{emoji} Battery is at {perc}%"
        )

        await interaction.response.send_message(
            embed=emb,
            allowed_mentions=nopings
        )