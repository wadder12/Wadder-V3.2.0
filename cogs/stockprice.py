import requests
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime
from nextcord.ui import button, View

class CustomView(View):
    def __init__(self, bot, stock_channel, timeout):
        super().__init__(timeout=None)
        self.bot = bot
        self.stock_channel = stock_channel

    @button(label="Previous", custom_id="previous", style=nextcord.ButtonStyle.green)
    async def previous_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.bot.dispatch("display_stocks", self.stock_channel, -1)

    @button(label="Next", custom_id="next", style=nextcord.ButtonStyle.green)
    async def next_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.bot.dispatch("display_stocks", self.stock_channel, 1)

class StockPrice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stock_channel = None
        self.ticker_message = None
        self.previous_stock_prices = {}
        self.stock_offset = 0
        self.bot.add_listener(self.on_display_stocks, "on_display_stocks")
        self.ticker_task.start()

    async def create_stock_channel(self, guild):
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False)
        }
        channel_name = "💹stock-prices"
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        return channel

    async def fetch_stocks(self, offset, limit):
        url = f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&offset={offset}&limit={limit}&apikey=demo"
        response = requests.get(url)
        data = response.json()
        return [stock["symbol"] for stock in data]

    async def fetch_stock_prices(self, symbols):
        stock_prices = {}
        for symbol in symbols:
            url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=demo"
            response = requests.get(url)
            data = response.json()[0]
            stock_prices[symbol] = data["price"]
        return stock_prices

    async def format_prices_embed(self, stock_prices):
        embed = nextcord.Embed(title="Stock Prices", color=0x2ecc71, timestamp=datetime.utcnow())
        embed.set_thumbnail(url="https://i.imgur.com/1xEviyL.png")  # You can replace this URL with your preferred thumbnail image

        symbols = [symbol.upper() for symbol in stock_prices.keys()]
        prices = [f"${round(price, 2)}" for price in stock_prices.values()]

        for i in range(0, len(symbols), 2):
            name_1 = symbols[i]
            value_1 = prices[i]
            try:
                name_2 = symbols[i + 1]
                value_2 = prices[i + 1]
            except IndexError:
                name_2 = '\u200b'  # Zero-width space character
                value_2 = '\u200b'  # Zero-width space character

            embed.add_field(name=name_1, value=value_1, inline=True)
            embed.add_field(name=name_2, value=value_2, inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)  # Adds an empty row

        embed.set_footer(text="Stock prices updated")
        return embed

    async def on_display_stocks(self, stock_channel, direction):
        self.stock_offset += direction * 50
        if self.stock_offset < 0:
            self.stock_offset = 0
            return

        stock_symbols = await self.fetch_stocks(self.stock_offset, 50)
        stock_prices = await self.fetch_stock_prices(stock_symbols)
        formatted_prices_embed = await self.format_prices_embed(stock_prices)
        await self.ticker_message.edit(embed=formatted_prices_embed)

    @tasks.loop(minutes=1)
    async def ticker_task(self):
        if self.stock_channel is None or self.ticker_message is None:
            return

        try:
            stock_symbols = await self.fetch_stocks(self.stock_offset, 50)
            stock_prices = await self.fetch_stock_prices(stock_symbols)
            formatted_prices_embed = await self.format_prices_embed(stock_prices)
            await self.ticker_message.edit(embed=formatted_prices_embed)

        except Exception as e:
            print(f"Error fetching stock prices: {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_stock_ticker(self, ctx):
        if self.stock_channel is not None:
            await ctx.send("A stock ticker channel already exists.")
            return

        self.stock_channel = await self.create_stock_channel(ctx.guild)
        stock_symbols = await self.fetch_stocks(self.stock_offset, 50)
        stock_prices = await self.fetch_stock_prices(stock_symbols)
        formatted_prices_embed = await self.format_prices_embed(stock_prices)
        self.ticker_message = await self.stock_channel.send(embed=formatted_prices_embed, view=CustomView(self.bot, self.stock_channel, timeout=86400))
        await ctx.send(f"Stock ticker channel created: {self.stock_channel.mention}")

    @commands.command()
    async def search_stock(self, ctx, query: str):
        url = f"https://financialmodelingprep.com/api/v3/search?query={query}&limit=10&apikey=demo"
        response = requests.get(url)
        data = response.json()

        if not data:
            await ctx.send("No results found.")
            return

        embed = nextcord.Embed(title=f"Search Results for '{query}'", color=0x2ecc71, timestamp=datetime.utcnow())

        for stock in data:
            embed.add_field(name=f"{stock['name']} ({stock['symbol']})", value=f"Exchange: {stock['stockExchange']}")

        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(StockPrice(bot))