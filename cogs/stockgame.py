import asyncio
import nextcord
from nextcord.ext import commands, tasks
import aiohttp
from nextcord.ui import Button, View
import json
import os
import random

class StockMarketGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.load_players()
        self.stocks = {}
        self.update_interests.start()
        self.bank = {"balance": 1000000, "loan_interest": 0.05, "savings_interest": 0.02}
        self.update_stock_prices.start()

    async def get_top_stocks(self, limit=50):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&limit={limit}&apikey=demo") as response:
                data = await response.json()
        return [stock["symbol"] for stock in data]
    async def get_random_stock(self):
        stock_symbols = list(self.stocks.keys())
        return random.choice(stock_symbols)
    
    
    def cog_unload(self):
        self.update_stock_prices.cancel()
    
    def save_players(self):
        with open("players.json", "w") as f:
            json.dump(self.players, f)

    def load_players(self):
        if os.path.exists("players.json"):
            with open("players.json", "r") as f:
                self.players = json.load(f)
        else:
            self.players = {}
    
    
    @tasks.loop(minutes=1)
    async def update_stock_prices(self):
        top_stocks = await self.get_top_stocks()
        async with aiohttp.ClientSession() as session:
            for stock in top_stocks:
                async with session.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey=demo") as response:
                    data = (await response.json())[0]
                self.stocks[stock] = {"price": data["price"], "name": data["name"], "changePercent": data["changesPercentage"]}
    
    @tasks.loop(minutes=30)  # You can change the interval to your preference
    async def update_interests(self):
        for player_id, player_data in self.players.items():
            player_data["savings"] *= (1 + self.bank["savings_interest"])
            player_data["loan"] *= (1 + self.bank["loan_interest"])
            
    def is_admin():
        async def predicate(ctx):
            return ctx.author.guild_permissions.administrator
        return commands.check(predicate)
    
    def calculate_net_worth(self, player_data):
        net_worth = player_data["balance"] + player_data["savings"] - player_data["loan"]
        for stock, quantity in player_data["portfolio"].items():
            net_worth += self.stocks[stock]["price"] * quantity
        return net_worth
    @commands.command()
    async def stocks(self, ctx):
        stocks_list = [f"{stock}: {self.stocks[stock]['name']} (${self.stocks[stock]['price']:.2f})" for stock in self.stocks]
        await ctx.send("Available stocks:\n" + "\n".join(stocks_list))

    @commands.command()
    async def stock_info(self, ctx, symbol: str):
        if symbol not in self.stocks:
            await ctx.send("That stock symbol is not available for trading.")
        else:
            stock_info = self.stocks[symbol]
            await ctx.send(f"{symbol}: {stock_info['name']} (${stock_info['price']:.2f})")

    @commands.command()
    async def join_game(self, ctx):
        player_id = str(ctx.author.id)
        if player_id in self.players:
            await ctx.send("You have already joined the game.")
        else:
            self.players[player_id] = {"balance": 100000, "portfolio": {}, "savings": 0, "loan": 0}
            await ctx.send(f"Welcome to the game, {ctx.author.mention}! You have been given $100,000 to start trading.")
            self.save_players()
    @commands.command()
    async def save_money(self, ctx, amount: float):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif amount <= 0:
            await ctx.send("Amount must be positive.")
        elif amount > self.players[player_id]["balance"]:
            await ctx.send("You do not have enough funds to save this amount.")
        else:
            self.players[player_id]["balance"] -= amount
            self.players[player_id]["savings"] += amount
            await ctx.send(f"You have successfully saved ${amount:.2f}.")
            self.save_players()
    @commands.command()
    async def take_loan(self, ctx, amount: float):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif amount <= 0:
            await ctx.send("Amount must be positive.")
        elif amount > self.bank["balance"]:
            await ctx.send("The bank does not have enough funds to give you this loan.")
        else:
            self.bank["balance"] -= amount
            self.players[player_id]["balance"] += amount
            self.players[player_id]["loan"] += amount * (1 + self.bank["loan_interest"])
            await ctx.send(f"You have successfully taken a loan of ${amount:.2f}. You need to pay back ${amount * (1 + self.bank['loan_interest']):.2f}.")
            self.save_players()
    @commands.command()
    async def pay_loan(self, ctx, amount: float):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif amount <= 0:
            await ctx.send("Amount must be positive.")
        elif amount > self.players[player_id]["balance"]:
            await ctx.send("You do not have enough funds to pay back this amount.")
        elif amount > self.players[player_id]["loan"]:
            await ctx.send("You are trying to pay back more than you owe.")
        else:
            self.players[player_id]["balance"] -= amount
            self.players[player_id]["loan"] -= amount
            await ctx.send(f"You have successfully paid back ${amount:.2f} of your loan.")
            self.save_players()
    @commands.command()
    @is_admin()
    async def bank_balance(self, ctx):
        balance = self.bank["balance"]
        await ctx.send(f"Bank balance: ${balance:.2f}")
    
    
    @commands.command()
    @is_admin()
    async def set_bank_balance(self, ctx, amount: float):
        if amount < 0:
            await ctx.send("Bank balance cannot be negative.")
        else:
            self.bank["balance"] = amount
            await ctx.send(f"Bank balance has been set to ${amount:.2f}.")

    @commands.command()
    @is_admin()
    async def set_interest_rates(self, ctx, loan_interest: float, savings_interest: float):
        if loan_interest < 0 or savings_interest < 0:
            await ctx.send("Interest rates cannot be negative.")
        else:
            self.bank["loan_interest"] = loan_interest
            self.bank["savings_interest"] = savings_interest
            await ctx.send(f"Loan interest rate has been set to {loan_interest * 100:.2f}% and savings interest rate has been set to {savings_interest * 100:.2f}%.")

    @commands.command()
    async def buy_stock(self, ctx, symbol: str, quantity: int):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif symbol not in self.stocks:
            await ctx.send("That stock symbol is not available for trading.")
        else:
            price = self.stocks[symbol]["price"]
            cost = price * quantity
            if cost > self.players[player_id]["balance"]:
                await ctx.send("You do not have enough funds to buy this many shares.")
            else:
                self.players[player_id]["balance"] -= cost
                if symbol in self.players[player_id]["portfolio"]:
                    self.players[player_id]["portfolio"][symbol] += quantity
                else:
                    self.players[player_id]["portfolio"][symbol] = quantity
                await ctx.send(f"You have successfully bought {quantity} shares of {symbol} for ${cost:.2f}.")
                self.save_players()
    @commands.command()
    async def sell_stock(self, ctx, symbol: str, quantity: int):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif symbol not in self.stocks:
            await ctx.send("That stock symbol is not available for trading.")
        elif symbol not in self.players[player_id]["portfolio"]:
            await ctx.send("You do not have any shares of this stock to sell.")
        elif quantity > self.players[player_id]["portfolio"][symbol]:
            await ctx.send("You do not have this many shares to sell.")
        else:
            price = self.stocks[symbol]["price"]
            proceeds = price * quantity
            self.players[player_id]["balance"] += proceeds
            self.players[player_id]["portfolio"][symbol] -= quantity
            if self.players[player_id]["portfolio"][symbol] == 0:
                del self.players[player_id]["portfolio"][symbol]
            await ctx.send(f"You have successfully sold {quantity} shares of {symbol} for ${proceeds:.2f}.")
            self.save_players()
    @commands.command()
    async def portfolio(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            portfolio = self.players[player_id]["portfolio"]
            portfolio_list = [f"{symbol}: {quantity} shares (${self.stocks[symbol]['price'] * quantity:.2f})" for symbol, quantity in portfolio.items()]
            loan_amount = self.players[player_id]["loan"]

            if not portfolio_list:
                await ctx.send("Your portfolio is empty.")
            else:
                await ctx.send("Your portfolio:\n" + "\n".join(portfolio_list) + f"\nLoan amount: ${loan_amount:.2f}")
                self.save_players()
    @commands.command()
    async def pbal(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            balance_embed = nextcord.Embed(title="Your Balance", description=f"${self.players[player_id]['balance']:.2f}", color=0x00ff00)
            await ctx.send(embed=balance_embed)
            self.save_players()
    @commands.command()
    async def leaderboard(self, ctx):
        sorted_players = sorted(self.players.items(), key=lambda x: self.calculate_net_worth(x[1]), reverse=True)
        leaderboard = []
        for player_id, player_data in sorted_players:
            user = self.bot.get_user(int(player_id))
            net_worth = self.calculate_net_worth(player_data)
            leaderboard.append(f"{user.display_name}: ${net_worth:.2f}")

        embed = nextcord.Embed(title="Stock Market Game Leaderboard", description="\n".join(leaderboard), color=0x00ff00)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def leave_game(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            del self.players[player_id]
            await ctx.send(f"You have left the game, {ctx.author.mention}. All your progress has been lost.")
            self.save_players()
            
            
    @commands.command()
    async def loan_status(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            loan_amount = self.players[player_id]["loan"]
            await ctx.send(f"Your current loan amount: ${loan_amount:.2f}")
            
            
    @commands.command()
    async def savings_status(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            savings_amount = self.players[player_id]["savings"]
            await ctx.send(f"Your current savings balance: ${savings_amount:.2f}")  
            
            
            
    @commands.command()
    async def withdraw_savings(self, ctx, amount: float):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        elif amount <= 0:
            await ctx.send("Amount must be positive.")
        elif amount > self.players[player_id]["savings"]:
            await ctx.send("You do not have enough funds in your savings to withdraw this amount.")
        else:
            self.players[player_id]["savings"] -= amount
            self.players[player_id]["balance"] += amount
            await ctx.send(f"You have successfully withdrawn ${amount:.2f} from your savings.")
            self.save_players()              




    @commands.command()
    async def top_movers(self, ctx):
        top_gainers = sorted(self.stocks.items(), key=lambda x: x[1]["changePercent"], reverse=True)[:5]
        top_losers = sorted(self.stocks.items(), key=lambda x: x[1]["changePercent"])[:5]

        gainers_list = [f"{stock[0]}: {stock[1]['name']} (${stock[1]['price']:.2f}, {stock[1]['changePercent']:.2f}%)" for stock in top_gainers]
        losers_list = [f"{stock[0]}: {stock[1]['name']} (${stock[1]['price']:.2f}, {stock[1]['changePercent']:.2f}%)" for stock in top_losers]

        await ctx.send("Top Gainers:\n" + "\n".join(gainers_list))
        await ctx.send("Top Losers:\n" + "\n".join(losers_list))





    @commands.command()
    async def stock_history(self, ctx, symbol: str, days: int = 7):
        if symbol not in self.stocks:
            await ctx.send("Invalid stock symbol.")
        else:
            history = await self.get_stock_history(symbol, days)
            history_list = [f"{date}: ${price:.2f}" for date, price in history.items()]
            await ctx.send(f"{self.stocks[symbol]['name']} ({symbol}) price history:\n" + "\n".join(history_list))

    @commands.command()
    async def liquidate_and_reset(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
        else:
            player_data = self.players[player_id]
            total_value = player_data["balance"]

            for stock_symbol, quantity in player_data["portfolio"].items():
                total_value += self.stocks[stock_symbol]["price"] * quantity

            self.players[player_id] = {"balance": total_value, "portfolio": {}, "savings": 0, "loan": 0}
            await ctx.send(f"{ctx.author.name}, you have liquidated all your stocks and reset your game progress. Your new balance is ${total_value:.2f}.")
            self.save_players()




    @commands.command()
    async def stock_challenge(self, ctx):
        player_id = str(ctx.author.id)
        if player_id not in self.players:
            await ctx.send("You have not joined the game yet.")
            return

        stock1 = await self.get_random_stock()
        stock2 = await self.get_random_stock()
        while stock1 == stock2:
            stock2 = await self.get_random_stock()

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in (stock1.lower(), stock2.lower())

        await ctx.send(f"Which stock will perform better in the next minute? Type your answer:\n1. {stock1}: {self.stocks[stock1]['name']}\n2. {stock2}: {self.stocks[stock2]['name']}")

        try:
            user_guess = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't respond in time!")
            return

        guessed_stock = user_guess.content.upper()
        initial_price1 = self.stocks[stock1]["price"]
        initial_price2 = self.stocks[stock2]["price"]

        await asyncio.sleep(60)

        final_price1 = self.stocks[stock1]["price"]
        final_price2 = self.stocks[stock2]["price"]

        performance1 = (final_price1 - initial_price1) / initial_price1
        performance2 = (final_price2 - initial_price2) / initial_price2

        if (guessed_stock == stock1 and performance1 > performance2) or (guessed_stock == stock2 and performance2 > performance1):
            reward = 100
            self.players[player_id]["balance"] += reward
            await ctx.send(f"Congratulations! You guessed correctly and earned ${reward:.2f}.")
        else:
            await ctx.send(f"Sorry, your guess was incorrect. Better luck next time!")



def setup(bot):
    bot.add_cog(StockMarketGame(bot))