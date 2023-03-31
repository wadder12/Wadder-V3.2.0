import nextcord
from nextcord.ext import commands
from collections import defaultdict


# add admin controls, and better embeds. 

class AuctionSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auctions = {}
        self.inventory = defaultdict(dict)
        self.currency = defaultdict(int)

    @commands.command()
    async def create_item(self, ctx, item_name: str, starting_price: int):
        if item_name in self.auctions:
            await ctx.send("An auction with this item name already exists.")
            return

        self.auctions[item_name] = {
            "starting_price": starting_price,
            "current_bid": starting_price,
            "highest_bidder": None
        }
        await ctx.send(f"Auction created for '{item_name}' with starting price {starting_price}.")

    @commands.command()
    async def bid(self, ctx, item_name: str, bid_amount: int):
        if item_name not in self.auctions:
            await ctx.send("This auction does not exist.")
            return

        auction = self.auctions[item_name]
        if bid_amount <= auction["current_bid"]:
            await ctx.send("Your bid must be higher than the current bid.")
            return

        user_id = str(ctx.author.id)
        if bid_amount > self.currency[user_id]:
            await ctx.send("You do not have enough virtual currency to place this bid.")
            return

        auction["current_bid"] = bid_amount
        auction["highest_bidder"] = ctx.author
        await ctx.send(f"{ctx.author.mention} is now the highest bidder with {bid_amount}.")
        
    @commands.command()
    async def end_auction(self, ctx, item_name: str):
        if item_name not in self.auctions:
            await ctx.send("This auction does not exist.")
            return

        auction = self.auctions[item_name]
        winner = auction["highest_bidder"]
        if winner is None:
            await ctx.send(f"No bids were placed for '{item_name}'. The auction has been closed.")
            del self.auctions[item_name]
            return

        winner_id = str(winner.id)
        item_cost = auction["current_bid"]
        self.currency[winner_id] -= item_cost
        if item_name in self.inventory[winner_id]:
            self.inventory[winner_id][item_name] += 1
        else:
            self.inventory[winner_id][item_name] = 1

        await ctx.send(f"{winner.mention} has won the auction for '{item_name}' at {item_cost}. The item has been added to their inventory.")
        del self.auctions[item_name]

    @commands.command()
    async def add_currency(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        self.currency[user_id] += amount
        await ctx.send(f"Added {amount} virtual currency to {ctx.author.mention}'s balance. New balance: {self.currency[user_id]}")

    @commands.command()
    async def show_inventory(self, ctx):
        user_id = str(ctx.author.id)
        inventory = self.inventory[user_id]

        if not inventory:
            await ctx.send("Your inventory is empty.")
            return

        inventory_display = "\n".join([f"{item}: {count}" for item, count in inventory.items()])
        await ctx.send(f"{ctx.author.mention}'s inventory:\n{inventory_display}")
    @commands.command()
    async def show_currency(self, ctx):
        user_id = str(ctx.author.id)
        balance = self.currency[user_id]
        await ctx.send(f"{ctx.author.mention}'s virtual currency balance: {balance}")
def setup(bot):
    bot.add_cog(AuctionSystem(bot))
    
    
    
    
#This cog provides an auction system where users can bid on items using virtual currency. It allows users to create items for auctions, place bids, end auctions, add currency to their balance, and display their inventory and currency balance.

#Note that this is a basic implementation and can be improved or extended as needed.