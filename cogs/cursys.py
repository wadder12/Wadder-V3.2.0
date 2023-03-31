import json
import os

import nextcord
from nextcord.ext import commands

# *need to come back and add roles to buy and make  a channel for this (bank) emperal=true 

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currency_data = {}
        self.data_file = "currency_data.json"
        self.load_currency_data()

    def load_currency_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.currency_data = json.load(f)

    def save_currency_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.currency_data, f)

    def get_currency(self, user_id):
        return self.currency_data.get(str(user_id), 0)

    def add_currency(self, user_id, amount):
        current_currency = self.get_currency(user_id)
        new_currency = current_currency + amount
        self.currency_data[str(user_id)] = new_currency
        self.save_currency_data()
        return new_currency

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            # Adjust this value to change how much currency is awarded per message sent
            currency_per_message = 1
            self.add_currency(message.author.id, currency_per_message)

    @commands.command()
    async def balance(self, ctx):
        balance = self.get_currency(ctx.author.id)
        embed = nextcord.Embed(title=f"{ctx.author.display_name}'s Balance", color=0x00ff00)
        embed.add_field(name="Balance", value=f"{balance} currency")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def award(self, ctx, user: nextcord.Member, amount: int):
        if amount < 1:
            await ctx.send("Amount must be at least 1.")
            return

        new_balance = self.add_currency(user.id, amount)
        embed = nextcord.Embed(title=f"Awarded {amount} currency to {user.display_name}", color=0x00ff00)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def take(self, ctx, user: nextcord.Member, amount: int):
        if amount < 1:
            await ctx.send("Amount must be at least 1.")
            return

        current_balance = self.get_currency(user.id)
        if current_balance < amount:
            await ctx.send(f"{user.display_name} doesn't have enough currency.")
            return

        new_balance = self.add_currency(user.id, -amount)
        embed = nextcord.Embed(title=f"Took {amount} currency from {user.display_name}", color=0xff0000)
        embed.add_field(name="New Balance", value=f"{new_balance} currency")
        await ctx.send(embed=embed)

    @commands.command()
    async def transfer(self, ctx, user: nextcord.Member, amount: int):
        if amount < 1:
            await ctx.send("Amount must be at least 1.")
            return

        current_balance = self.get_currency(ctx.author.id)
        if current_balance < amount:
            await ctx.send(f"You don't have enough currency.")
            return

        new_balance_sender = self.add_currency(ctx.author.id, -amount)
        new_balance_receiver = self.add_currency(user.id, amount)

        embed = nextcord.Embed(title=f"Transferred {amount} currency to {user.display_name}", color=0xffff00)
        embed.add_field(name=f"{ctx.author.display_name}'s New Balance", value=f"{new_balance_sender} currency")
        embed.add_field(name=f"{user.display_name}'s New Balance", value=f"{new_balance_receiver} currency")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Currency(bot))