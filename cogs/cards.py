import random
import nextcord
from nextcord.ext import commands

#pretty good!

class CardsAgainstHumanity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.black_cards = ["____? There's an app for that.", "Why am I sticky? ____."]
        self.white_cards = [
    "Flying robots that kill people",
    "A man on the brink of orgasm",
    "A passionate Latino lover",
    "A can of whoop-ass",
    "The American Dream",
    "Puppies!",
    "A tiny horse",
    "The Little Engine That Could",
    "Being fabulous",
    "The glass ceiling",
    "The invisible hand",
    "The Great Depression",
    "A pyramid of severed heads",
    "Funky fresh rhymes",
    "A Gypsy curse",
    "A moment of silence",
    "Party poopers",
    "A cooler full of organs",
    "A time travel paradox",
    "Soup that is too hot",
]
        self.active_games = {}

    @commands.command()
    async def cah_start(self, ctx):
        if ctx.channel.id in self.active_games:
            await ctx.send("A game of Cards Against Humanity is already in progress in this channel.")
            return

        self.active_games[ctx.channel.id] = {
            "players": [ctx.author],
            "black_card": None,
            "white_cards": {}
        }

        await ctx.send("A new game of Cards Against Humanity has started! Type /cah_join to join the game.")

    @commands.command()
    async def cah_join(self, ctx):
        if ctx.channel.id not in self.active_games:
            await ctx.send("No active Cards Against Humanity game in this channel. Start a game with !cah_start.")
            return

        if ctx.author not in self.active_games[ctx.channel.id]["players"]:
            self.active_games[ctx.channel.id]["players"].append(ctx.author)
            await ctx.send(f"{ctx.author.mention} has joined the game.")
        else:
            await ctx.send("You are already in the game.")

    @commands.command()
    async def cah_play(self, ctx):
        if ctx.channel.id not in self.active_games:
            await ctx.send("No active Cards Against Humanity game in this channel. Start a game with /cah_start.")
            return

        game = self.active_games[ctx.channel.id]

        if not game["black_card"]:
            game["black_card"] = random.choice(self.black_cards)

        for player in game["players"]:
            cards = random.sample(self.white_cards, 5)
            game["white_cards"][player] = cards
            await player.send(f"Black card: {game['black_card']}\nYour white cards: {', '.join(cards)}")

        await ctx.send(f"Black card: {game['black_card']}")
        await ctx.send("Check your DMs for your white cards. Type !cah_choose [number] to choose a card.")

    @commands.command()
    async def cah_choose(self, ctx, index: int):
        if ctx.channel.id not in self.active_games:
            await ctx.send("No active Cards Against Humanity game in this channel. Start a game with /cah_start.")
            return

        game = self.active_games[ctx.channel.id]

        if ctx.author not in game["white_cards"]:
            await ctx.send("You are not participating in this round.")
            return

        if index < 1 or index > 5:
            await ctx.send("Invalid card index. Choose a number between 1 and 5.")
            return

        # This part only shows the chosen card, you need to implement voting and determining the winner.
        chosen_card = game["white_cards"][ctx.author][index - 1]
        await ctx.send(f"{ctx.author.mention} chose: {chosen_card}")

def setup(bot):
    bot.add_cog(CardsAgainstHumanity(bot))