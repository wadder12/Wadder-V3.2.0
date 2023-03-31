import random
import asyncio
from nextcord.ext import commands

class MathChallenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.math_operations = ['+', '-', '*', '/']

    async def generate_math_problem(self):
        op = random.choice(self.math_operations)
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        else:
            num1 *= num2  # To avoid floating-point division
            result = num1 // num2

        return f"{num1} {op} {num2}", result

    @commands.command()
    async def mc(self, ctx):
        problem, answer = await self.generate_math_problem()
        await ctx.send(f"Solve this math problem: {problem}")

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and not m.author.bot

        try:
            response = await self.bot.wait_for('message', check=check, timeout=20)  # 20 seconds time limit
            if int(response.content) == answer:
                await ctx.send(f"Correct, {ctx.author.mention}! The answer is {answer}.")
            else:
                await ctx.send(f"Sorry, {ctx.author.mention}. The correct answer is {answer}.")
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The correct answer was {answer}.")

def setup(bot):
    bot.add_cog(MathChallenge(bot))