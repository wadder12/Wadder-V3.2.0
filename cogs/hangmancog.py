import random
import nextcord
from nextcord.ext import commands

# needs some serious work and more words!

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ["apple", "banana", "grape", "orange", "watermelon"]
        self.active_games = {}

    @commands.command()
    async def hangman(self, ctx):
        if ctx.channel.id in self.active_games:
            await ctx.send("A game of hangman is already in progress in this channel.")
            return

        word = random.choice(self.words)
        display = ["_" if letter.isalnum() else letter for letter in word]
        guesses = []

        self.active_games[ctx.channel.id] = {
            "word": word,
            "display": display,
            "guesses": guesses
        }

        await ctx.send("A new game of hangman has started!")
        await ctx.send(" ".join(display))

    @commands.command()
    async def guess(self, ctx, letter: str):
        if ctx.channel.id not in self.active_games:
            await ctx.send("No active hangman game in this channel. Start a game with !hangman.")
            return

        game = self.active_games[ctx.channel.id]

        if letter.lower() in game["guesses"]:
            await ctx.send("This letter has already been guessed!")
            return

        game["guesses"].append(letter.lower())

        if letter.lower() in game["word"].lower():
            for idx, char in enumerate(game["word"]):
                if char.lower() == letter.lower():
                    game["display"][idx] = char

            await ctx.send("Correct guess!")
        else:
            await ctx.send("Incorrect guess!")

        await ctx.send(" ".join(game["display"]))

        if "_" not in game["display"]:
            await ctx.send("Congratulations! You've guessed the word!")
            del self.active_games[ctx.channel.id]

    @commands.command()
    async def endhangman(self, ctx):
        if ctx.channel.id not in self.active_games:
            await ctx.send("No active hangman game in this channel.")
            return

        await ctx.send(f"The game has been ended. The word was: {self.active_games[ctx.channel.id]['word']}")
        del self.active_games[ctx.channel.id]

def setup(bot):
    bot.add_cog(Hangman(bot))